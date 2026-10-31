아래 Pine Script v6 전략을 개선해 주세요.

[개선 요구]
1. 익절 주문 대신, 진입 후 가격이 ATR × 1만큼 오르면 작동하는 트레일링 스톱(최고가에서 ATR × 1.5 하락 시 청산)으로 바꿉니다.
2. 최근 청산된 20건 거래의 승률(%)과 평균 수익률(%)을 차트 오른쪽 위 표에 표시합니다. 청산된 거래가 20건보다 적으면 있는 만큼만 계산합니다.
3. 나머지 규칙(진입 조건, 손절, 시간 청산, strategy 설정)은 그대로 둡니다.

[출력 형식]
- 전체 코드를 ```pine 코드 블록 하나로 주세요. 첫 줄은 //@version=6 입니다.

[현재 코드]
```pine
//@version=6
strategy("RSI 과매도 반등 매수 전략", overlay=true,
     initial_capital=10000000, currency=currency.KRW,
     default_qty_type=strategy.percent_of_equity, default_qty_value=100,
     commission_type=strategy.commission.percent, commission_value=0.165,
     slippage=0, process_orders_on_close=false)

rsiLength = input.int(14, "RSI 기간", minval=1)
rsiLevel = input.float(30.0, "RSI 기준선", minval=0.0, maxval=100.0)
bbLength = input.int(20, "볼린저밴드 기간", minval=1)
bbMultiplier = input.float(2.0, "표준편차 배수", minval=0.0, step=0.1)

rsi = ta.rsi(close, rsiLength)
basis = ta.sma(close, bbLength)
deviation = bbMultiplier * ta.stdev(close, bbLength)
upper = basis + deviation
lower = basis - deviation
atr = ta.atr(14)

rsiCrossUp = ta.crossover(rsi, rsiLevel)
buySignal = barstate.isconfirmed and rsiCrossUp and close > lower

// 다음 봉 시가 체결 전 마지막으로 확정된 ATR을 고정합니다.
var float entryAtr = na
if buySignal and strategy.position_size == 0 and not na(atr)
    entryAtr := atr
    strategy.entry("Long", strategy.long)

// 체결가를 기준으로 고정 손절·익절 주문을 유지합니다.
float stopPrice = strategy.position_size > 0 ? strategy.position_avg_price - entryAtr * 2.0 : na
float takePrice = strategy.position_size > 0 ? strategy.position_avg_price + entryAtr * 3.0 : na

if strategy.position_size > 0
    strategy.exit("손절/익절", "Long", stop=stopPrice, limit=takePrice)

    // 진입 봉부터 10개 봉이 완료되면 다음 봉 시가에 시장가 청산합니다.
    int entryBar = strategy.opentrades.entry_bar_index(0)
    if bar_index - entryBar >= 9
        strategy.close("Long", comment="시간 청산")

plot(upper, "볼린저밴드 상단", color=color.blue)
plot(basis, "볼린저밴드 중심선", color=color.orange)
plot(lower, "볼린저밴드 하단", color=color.blue)
plot(stopPrice, "손절가", color=color.blue, style=plot.style_linebr)
plot(takePrice, "익절가", color=color.red, style=plot.style_linebr)

plotshape(buySignal, title="매수 신호", style=shape.triangleup,
     location=location.belowbar, color=color.red, size=size.small)

alertcondition(buySignal, title="RSI 반등 매수", message="RSI 반등 매수 신호가 확정되었습니다.")
```
