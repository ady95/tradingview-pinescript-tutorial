아래 Pine Script v5 전략을 v6로 변환해 주세요.

[요구]
- 백테스트 결과(진입·청산 시점, 수량, 성과)가 v5와 똑같이 나오도록 합니다.
- v5와 v6 사이에 동작이 달라지는 부분(정수 나눗셈, bool과 na, 숫자의 bool 변환, when 인수, strategy의 기본 설정값 변화 등)을 모두 점검하고, 바꾼 이유를 코드 주석으로 남깁니다.
- 전체 코드를 ```pine 코드 블록 하나로 주세요.

```pine
//@version=5
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
