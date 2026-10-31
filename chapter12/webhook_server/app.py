"""TradingView Webhook을 받아 검증하고 키움 모의투자로 주문하는 서버 (12장).

실행:  uvicorn app:app --host 0.0.0.0 --port 8000
긴급 중단: 이 폴더에 STOP 파일을 만들면 이후 모든 신호를 거부한다.
"""
import hmac
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Literal

import httpx
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field, ValidationError

from kiwoom_client import KiwoomClient, KiwoomError
from settings import load_settings

BASE_DIR = Path(__file__).resolve().parent
AUDIT_LOG = BASE_DIR / "audit.jsonl"
STOP_FILE = BASE_DIR / "STOP"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("webhook")

settings = load_settings()
kiwoom = KiwoomClient(settings.kiwoom_base_url, settings.app_key, settings.app_secret)
app = FastAPI()


class Signal(BaseModel):
    strategy: str
    action: Literal["buy", "sell"]
    ticker: str = Field(pattern=r"^\d{6}$")
    exchange: Literal["KRX"]
    qty: int = Field(gt=0)
    price: float = Field(gt=0)
    bar_time: int
    signal_id: str


class Webhook(BaseModel):
    secret: str
    signal: Signal


def audit(event: str, **fields) -> None:
    """모든 수신·판단·주문을 한 줄 JSON으로 남긴다 (감사 로그)."""
    record = {"time": datetime.now().isoformat(timespec="seconds"), "event": event, **fields}
    with AUDIT_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def processed_ids() -> set:
    """감사 로그에서 이미 처리한 신호 ID를 읽는다. 서버를 다시 켜도 중복 주문을 막는다."""
    if not AUDIT_LOG.exists():
        return set()
    ids = set()
    for line in AUDIT_LOG.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        if record["event"] in ("accepted", "ordered", "dry_run"):
            ids.add(record.get("signal_id"))
    return ids


_day_start_value: dict = {}


def check_daily_loss() -> None:
    """오늘 첫 신호 때의 추정 예탁자산과 비교해 손실 한도를 넘으면 거부한다."""
    today = datetime.now().strftime("%Y-%m-%d")
    value = kiwoom.account_value()
    start = _day_start_value.setdefault(today, value)
    if start - value > settings.max_daily_loss:
        raise HTTPException(403, f"일일 손실 한도 초과: {start - value:,}원")


@app.post("/webhook")
async def webhook(request: Request):
    raw = await request.body()  # TradingView는 text/plain으로 보내므로 직접 JSON을 해석한다
    try:
        payload = Webhook.model_validate_json(raw)
    except ValidationError as e:
        audit("rejected", reason="형식 오류", detail=str(e.errors()[:3]))
        raise HTTPException(400, "잘못된 신호 형식")

    if not hmac.compare_digest(payload.secret, settings.webhook_secret):
        audit("rejected", reason="비밀값 불일치")
        raise HTTPException(401, "인증 실패")

    s = payload.signal
    if STOP_FILE.exists():
        audit("rejected", reason="긴급 중단", signal_id=s.signal_id)
        raise HTTPException(503, "긴급 중단 상태")
    if s.signal_id in processed_ids():
        audit("rejected", reason="중복 신호", signal_id=s.signal_id)
        return {"status": "duplicate"}
    if s.ticker not in settings.allowed_tickers:
        audit("rejected", reason="허용되지 않은 종목", signal_id=s.signal_id, ticker=s.ticker)
        raise HTTPException(403, "허용되지 않은 종목")
    amount = int(s.qty * s.price)
    if amount > settings.max_order_amount:
        audit("rejected", reason="주문 금액 한도 초과", signal_id=s.signal_id, amount=amount)
        raise HTTPException(403, "주문 금액 한도 초과")

    if settings.dry_run:
        audit("dry_run", signal_id=s.signal_id, action=s.action, ticker=s.ticker, qty=s.qty, amount=amount)
        return {"status": "dry_run", "signal_id": s.signal_id}

    try:
        check_daily_loss()
        audit("accepted", signal_id=s.signal_id, action=s.action, ticker=s.ticker, qty=s.qty, amount=amount)
        order_no = kiwoom.order(s.action, s.ticker, s.qty)  # 시장가
    except HTTPException:
        audit("rejected", reason="일일 손실 한도 초과", signal_id=s.signal_id)
        raise
    except (KiwoomError, httpx.HTTPError) as e:
        audit("order_failed", signal_id=s.signal_id, error=str(e))
        raise HTTPException(502, f"주문 실패: {e}")
    audit("ordered", signal_id=s.signal_id, order_no=order_no)
    log.info("주문 완료 %s %s %s주 (주문번호 %s)", s.action, s.ticker, s.qty, order_no)
    return {"status": "ordered", "order_no": order_no}


@app.get("/health")
def health():
    return {"status": "stopped" if STOP_FILE.exists() else "ok", "dry_run": settings.dry_run}
