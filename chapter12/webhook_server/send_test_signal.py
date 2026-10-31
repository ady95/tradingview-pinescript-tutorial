"""TradingView 대신 테스트 신호를 보내 서버를 점검한다 (12장).

사용법:  python send_test_signal.py buy 005930 1
"""
import json
import os
import sys
import time

import httpx

from settings import load_settings

settings = load_settings()
action, ticker, qty = sys.argv[1], sys.argv[2], int(sys.argv[3])
bar_time = int(time.time() // 86400 * 86400 * 1000)
message = {
    "secret": settings.webhook_secret,
    "signal": {
        "strategy": "trend_v1",
        "action": action,
        "ticker": ticker,
        "exchange": "KRX",
        "qty": qty,
        "price": float(os.environ.get("TEST_PRICE", "225000")),
        "bar_time": bar_time,
        "signal_id": f"trend_v1-{action}-{ticker}-{bar_time}",
    },
}
url = os.environ.get("WEBHOOK_URL", "http://127.0.0.1:8000/webhook")
# TradingView처럼 text/plain 본문으로 보낸다
response = httpx.post(url, content=json.dumps(message), headers={"Content-Type": "text/plain; charset=utf-8"})
print(response.status_code, response.text)
