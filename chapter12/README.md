# 12장. Webhook 기반 자동매매 연동 따라하기

이 장의 예제 코드입니다. 각 파일은 책 본문의 해당 절과 같은 코드입니다.

| 파일 | 본문 절 | 설명 |
|---|---|---|
| alert_strategy.pine | 12-1, 12-2 | 주문 알림에 JSON 신호(alert_message)를 싣는 전략 |
| webhook_server/settings.py | 12-3 | 환경변수 설정 읽기 |
| webhook_server/app.py | 12-3, 12-4 | Webhook 수신·인증·중복 방지·리스크 검증·감사 로그·긴급 중단 |
| webhook_server/kiwoom_client.py | 12-4 | 키움증권 REST API 모의투자 클라이언트 (토큰·예수금·잔고·주문·취소) |
| webhook_server/send_test_signal.py | 12-3, 12-5 | TradingView 대신 테스트 신호 보내기 |
| webhook_server/requirements.txt | 12-3 | 필요한 패키지 |
