"""12장 모의매매 서버의 상태를 읽기 전용으로 보여 주는 MCP 서버 (13장).

제공 도구 (모두 읽기 전용, 주문 기능 없음):
    server_status   긴급 중단(STOP) 여부와 DRY_RUN 설정
    audit_summary   감사 로그의 이벤트 수와 거부 사유 집계
    recent_audit    최근 감사 로그 (주문번호는 지우고 돌려줌)
    paper_balance   키움 모의투자 예수금·추정 예탁자산 조회

Claude Code에 등록 (chapter13 폴더에서 실행):
    claude mcp add paper-trading -- python paper_mcp/server.py

환경변수: KIWOOM_PAPER_APP_KEY, KIWOOM_PAPER_APP_SECRET (paper_balance에만 필요)
12장과 같이 예제 저장소 루트의 .env 또는 셸 환경변수에서 읽는다.
"""
import json
import os
import sys
from collections import Counter
from pathlib import Path

from mcp.server import MCPServer
from mcp.types import ToolAnnotations

REPO_DIR = Path(__file__).resolve().parent.parent.parent
CH12_DIR = REPO_DIR / "chapter12" / "webhook_server"
sys.path.insert(0, str(CH12_DIR))

# 12장 클라이언트를 그대로 쓴다
from kiwoom_client import KiwoomClient  # noqa: E402
from settings import load_dotenv  # noqa: E402

AUDIT_LOG = CH12_DIR / "audit.jsonl"
STOP_FILE = CH12_DIR / "STOP"
READ_ONLY = ToolAnnotations(readOnlyHint=True, destructiveHint=False)
HIDDEN_FIELDS = {"order_no"}  # AI에게 넘길 필요가 없는 값

load_dotenv(REPO_DIR / ".env")

mcp = MCPServer(
    "paper-trading",
    instructions=(
        "12장 모의매매 서버의 감사 로그와 키움 모의투자 잔고를 "
        "읽기만 합니다. 주문 도구는 없습니다."
    ),
)


def read_audit() -> list[dict]:
    """감사 로그(audit.jsonl)를 읽는다. 깨진 줄은 건너뛴다."""
    if not AUDIT_LOG.exists():
        return []
    records = []
    for line in AUDIT_LOG.read_text(encoding="utf-8").splitlines():
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records


@mcp.tool(annotations=READ_ONLY)
def server_status() -> dict:
    """모의매매 서버의 상태를 알려 준다.

    긴급 중단(STOP 파일) 여부, DRY_RUN 설정, 감사 로그 줄 수.
    """
    return {
        "stopped": STOP_FILE.exists(),
        "dry_run": os.environ.get("DRY_RUN", "true").lower() != "false",
        "audit_records": len(read_audit()),
    }


@mcp.tool(annotations=READ_ONLY)
def audit_summary(date: str = "") -> dict:
    """감사 로그의 이벤트별 건수와 거부 사유별 건수를 센다.

    date(YYYY-MM-DD)를 주면 그날만 센다.
    """
    records = [r for r in read_audit() if r.get("time", "").startswith(date)]
    return {
        "date": date or "전체",
        "total": len(records),
        "events": dict(Counter(r.get("event", "") for r in records)),
        "rejected_reasons": dict(Counter(
            r.get("reason", "")
            for r in records if r.get("event") == "rejected"
        )),
    }


@mcp.tool(annotations=READ_ONLY)
def recent_audit(limit: int = 20, event: str = "") -> list[dict]:
    """최근 감사 로그를 최신순으로 돌려준다.

    event로 accepted·ordered·rejected·order_failed 등을 거를 수 있다.
    """
    limit = max(1, min(limit, 200))
    records = [r for r in read_audit() if not event or r.get("event") == event]
    return [
        {k: v for k, v in r.items() if k not in HIDDEN_FIELDS}
        for r in reversed(records[-limit:])
    ]


@mcp.tool(annotations=READ_ONLY)
def paper_balance() -> dict:
    """키움 모의투자 계좌의 예수금·주문가능금액·추정 예탁자산(원)을 조회한다."""
    client = KiwoomClient(
        os.environ.get("KIWOOM_BASE_URL", "https://mockapi.kiwoom.com"),
        os.environ.get("KIWOOM_PAPER_APP_KEY", ""),
        os.environ.get("KIWOOM_PAPER_APP_SECRET", ""),
    )
    return {**client.deposit(), "account_value": client.account_value()}


if __name__ == "__main__":
    mcp.run()  # 표준 입출력(stdio)으로 Claude Code와 통신한다
