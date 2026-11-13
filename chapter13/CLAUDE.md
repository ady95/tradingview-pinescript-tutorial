# 13장 실습 규칙 (Claude Code가 읽는 파일)

이 폴더에서는 TradingView 공식 MCP(mcp-tradingview)로 Pine Script를 검증·백테스트한다.

## Pine Script 작업 순서

1. 코드는 Pine Script v6로 쓰고 첫 줄은 `//@version=6`로 한다.
2. 코드를 보여 주기 전에 반드시 `validate-pine-script`로 검증한다. 오류가 있으면 고쳐서 다시 검증하고, 몇 번 고쳤는지 기록한다.
3. 전략은 `run-pine-backtest`로 실행한다. 기본값: KRX:005930, 1D, 날짜 미지정(차트 전체 기간).
4. Pine 실행 도구(run-pine-indicator, run-pine-backtest)는 동시에 2개까지만 부른다.

## 결과 보고

- 백테스트 결과의 *_percent 값과 percent_profitable은 비율(0.25 = 25%)이다. 100을 곱해 보여 준다.
- 순손익·최대 손실폭·승률(이긴 거래/전체 거래)·Profit Factor·테스트 기간(report.range)을 표로 보고한다.
- 도구가 돌려준 원래 숫자를 함께 적는다. 반올림했으면 반올림했다고 적는다.
- 컴파일 경고(warnings)도 빠뜨리지 않고 보고한다.
- 전략의 좋고 나쁨을 투자 권유처럼 말하지 않는다.

## 금지

- 계정에 저장하거나 바꾸는 도구(create/update-pine-script, 알림·관심종목 변경)는 쓰지 않는다.
- request.security()로 미래 데이터를 참조하지 않는다.
