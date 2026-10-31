아래 Pine Script v6 지표를 백테스트할 수 있는 strategy 스크립트로 바꿔 주세요.

[유지할 것]
- 매수 신호 조건(RSI 30 상향 돌파 + 종가 > 볼린저밴드 하단, 확정봉 기준)

[추가할 것]
- 진입: 매수 신호가 난 캔들의 다음 캔들 시가에 롱 진입 (기본 체결 방식 사용)
- 손절: 진입 시점 ATR(14) × 2 아래
- 익절: 진입 시점 ATR(14) × 3 위
- 시간 청산: 진입 후 10캔들이 지나도 청산되지 않았으면 시장가 청산
- strategy() 설정: 초기 자본 10,000,000원(KRW), 자본의 100% 주문, 수수료 0.165%(퍼센트), 슬리피지 0
- 포지션이 있을 때 손절가(파란색)와 익절가(빨간색)를 선으로 표시

[금지]
- request.security() 사용 금지, 미래 데이터 참조 금지
- ta 함수를 if 블록 안에서 호출하지 않기

[출력 형식]
- 전체 코드를 ```pine 코드 블록 하나로 주세요. 첫 줄은 //@version=6 입니다.

[원본 지표]
```pine
//@version=6
indicator("RSI 과매도 반등 매수 신호", overlay=true)

rsiLength = input.int(14, "RSI 기간", minval=1)
rsiLevel = input.float(30.0, "RSI 기준선", minval=0.0, maxval=100.0)
bbLength = input.int(20, "볼린저밴드 기간", minval=1)
bbMultiplier = input.float(2.0, "표준편차 배수", minval=0.0, step=0.1)

rsi = ta.rsi(close, rsiLength)
basis = ta.sma(close, bbLength)
deviation = bbMultiplier * ta.stdev(close, bbLength)
upper = basis + deviation
lower = basis - deviation

rsiCrossUp = ta.crossover(rsi, rsiLevel)
buySignal = barstate.isconfirmed and rsiCrossUp and close > lower

plot(upper, "볼린저밴드 상단", color=color.blue)
plot(basis, "볼린저밴드 중심선", color=color.orange)
plot(lower, "볼린저밴드 하단", color=color.blue)

plotshape(buySignal, title="매수 신호", style=shape.triangleup, location=location.belowbar, color=color.red, size=size.small)

alertcondition(buySignal, title="RSI 반등 매수", message="RSI 반등 매수 신호가 확정되었습니다.")
```
