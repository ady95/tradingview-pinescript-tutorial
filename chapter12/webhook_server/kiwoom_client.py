"""키움증권 REST API 모의투자 클라이언트 (12장). 주문·조회에 필요한 최소 기능만 담았다."""
import time

import httpx


class KiwoomError(Exception):
    pass


class KiwoomClient:
    def __init__(self, base_url: str, app_key: str, app_secret: str) -> None:
        if "mockapi" not in base_url:
            raise ValueError("이 예제는 모의투자 도메인(mockapi.kiwoom.com)에서만 동작합니다.")
        self.base_url = base_url.rstrip("/")
        self.app_key = app_key
        self.app_secret = app_secret
        self._token = ""
        self._token_time = 0.0
        self._http = httpx.Client(timeout=10)

    def _get_token(self) -> str:
        # 토큰은 발급 후 일정 시간 유효하므로, 6시간마다 새로 받는다
        if self._token and time.time() - self._token_time < 6 * 3600:
            return self._token
        data = self._post("/oauth2/token", {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "secretkey": self.app_secret,
        })
        self._token, self._token_time = data["token"], time.time()
        return self._token

    def _post(self, path: str, body: dict, api_id: str = "") -> dict:
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        if api_id:
            headers["api-id"] = api_id
            headers["authorization"] = f"Bearer {self._get_token()}"
        response = self._http.post(self.base_url + path, json=body, headers=headers)
        response.raise_for_status()
        data = response.json()
        if str(data.get("return_code")) != "0":
            raise KiwoomError(f"{api_id or path}: {data.get('return_msg')}")
        return data

    def deposit(self) -> dict:
        """예수금·주문가능금액 조회 (kt00001)."""
        data = self._post("/api/dostk/acnt", {"qry_tp": "3"}, "kt00001")
        return {"cash": int(data["entr"]), "orderable": int(data["ord_alow_amt"])}

    def account_value(self) -> int:
        """추정 예탁자산 (kt00018). 일일 손실 한도 계산에 쓴다."""
        data = self._post("/api/dostk/acnt", {"qry_tp": "1", "dmst_stex_tp": "KRX"}, "kt00018")
        return int(data["prsm_dpst_aset_amt"])

    def order(self, side: str, ticker: str, qty: int, price: int = 0) -> str:
        """매수(kt10000)·매도(kt10001) 주문. price=0이면 시장가, 아니면 지정가. 주문번호를 돌려준다."""
        api_id = "kt10000" if side == "buy" else "kt10001"
        body = {
            "dmst_stex_tp": "KRX",
            "stk_cd": ticker,
            "ord_qty": str(qty),
            "ord_uv": str(price) if price else "",
            "trde_tp": "0" if price else "3",  # 0: 보통(지정가), 3: 시장가
            "cond_uv": "",
        }
        return self._post("/api/dostk/ordr", body, api_id)["ord_no"]

    def cancel(self, ticker: str, order_no: str) -> str:
        """미체결 주문 전량 취소 (kt10003)."""
        body = {"dmst_stex_tp": "KRX", "orig_ord_no": order_no, "stk_cd": ticker, "cncl_qty": "0"}
        return self._post("/api/dostk/ordr", body, "kt10003")["ord_no"]
