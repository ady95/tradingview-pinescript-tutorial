TradingView MCP로 국내 주식 후보를 골라 줘. 계정에 저장하거나 바꾸는 도구는 쓰지 마.

1단계 — run-screener
- market: korea, symbol_types: ["stock"]
- 필터: relative_volume_10d_calc 3 이상, Value.Traded 50억(5000000000) 이상, change 0 이상
- 정렬: Value.Traded 내림차순, limit 50
- totalCount와 실제 받은 행 수를 함께 알려 줘.

2단계 — run-pine-indicator
- 1단계 후보 전부에 chapter07/volume_breakout_screener.pine 코드를 그대로 넘겨 실행해 (timeframe 1D, return_bars 1).
- plot "후보"가 1인 종목만 표로 정리해: 심볼, 막대 날짜, 거래량 배수, 신고가 대비(%), EMA 이격도(%), 거래대금(억).

주의
- 숫자는 도구가 돌려준 값을 그대로 옮기고, 계산하거나 반올림했다면 그렇게 적어 줘.
- 보통주와 우선주가 함께 나오면 따로 표시해 줘.
- 매수·매도 의견은 쓰지 마.
