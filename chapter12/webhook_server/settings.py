"""환경변수 설정 읽기 (12장). 값은 .env 파일이나 셸 환경변수로 넣는다."""
import os
from dataclasses import dataclass
from pathlib import Path


def load_dotenv(path: Path) -> None:
    """의존 패키지 없이 .env 파일의 KEY=VALUE를 환경변수로 읽는다."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


@dataclass(frozen=True)
class Settings:
    webhook_secret: str
    kiwoom_base_url: str
    app_key: str
    app_secret: str
    max_order_amount: int
    max_daily_loss: int
    allowed_tickers: frozenset
    max_signal_age_hours: float
    dry_run: bool


def load_settings() -> Settings:
    load_dotenv(Path(".env"))
    load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")
    secret = os.environ.get("WEBHOOK_SECRET", "")
    if len(secret) < 16 or not secret.isascii():
        raise RuntimeError("WEBHOOK_SECRET을 16자 이상의 영문·숫자로 설정하세요.")
    tickers = os.environ.get("ALLOWED_TICKERS", "005930,000660")
    return Settings(
        webhook_secret=secret,
        kiwoom_base_url=os.environ.get("KIWOOM_BASE_URL", "https://mockapi.kiwoom.com"),
        app_key=os.environ.get("KIWOOM_PAPER_APP_KEY", ""),
        app_secret=os.environ.get("KIWOOM_PAPER_APP_SECRET", ""),
        max_order_amount=int(os.environ.get("MAX_ORDER_AMOUNT_KRW", "1000000")),
        max_daily_loss=int(os.environ.get("MAX_DAILY_LOSS_KRW", "300000")),
        allowed_tickers=frozenset(t.strip() for t in tickers.split(",") if t.strip()),
        max_signal_age_hours=float(os.environ.get("MAX_SIGNAL_AGE_HOURS", "24")),
        dry_run=os.environ.get("DRY_RUN", "true").lower() != "false",
    )
