아래 Pine Script를 //@version=6 으로 컴파일하면 오류가 납니다. 오류를 고친 전체 코드를 주세요.
동작(진입·청산 조건과 결과)은 원래 의도와 같게 유지하고, 무엇을 왜 고쳤는지 코드 주석으로 짧게 남겨 주세요.

[컴파일 오류]
"문제 7개 중 1개 Cannot assign a value of the \"simple na\" type to the \"trendOk\" variable. The variable is declared with the \"const bool\" type.(CE10173)\n문제 7개 중 2개 Cannot assign a value of the \"simple na\" type to the \"trendOk\" variable. The variable is declared with the \"const bool\" type.(CE10173)"

[코드]
```pine
//@version=6
strategy("v5 예제 — 거래량 돌파", overlay = true, initial_capital = 10000000, currency = currency.KRW, default_qty_type = strategy.percent_of_equity, default_qty_value = 100)

len = input.int(15, "기간", minval = 2)
half = len / 2
ma = ta.sma(close, half)
volAvg = ta.sma(volume, 20)

// v5에서는 bool 변수에 na를 넣을 수 있다
var bool trendOk = na
trendOk := close > ma

// v5에서는 숫자를 조건에 바로 쓸 수 있다 (0이면 거짓)
hasVolume = volume ? true : false
volUp = hasVolume and volume > volAvg * 2

// v5에서는 when 인수로 조건부 주문을 낼 수 있다
strategy.entry("L", strategy.long, when = ta.crossover(close, ma) and volUp)
strategy.close("L", when = ta.crossunder(close, ma))

plot(ma, "이동평균", color = color.orange)
```
