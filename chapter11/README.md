# 11장. AI로 Pine Script 개발하기

이 장의 예제 코드입니다. 각 파일은 책 본문의 해당 절과 같은 코드입니다.

| 파일 | 본문 절 | 설명 |
|---|---|---|
| ai_pine_request.py | 11-1 | 프롬프트 파일을 보내 Pine Script 초안을 받는 스크립트 (OPENAI_API_KEY·OPENAI_MODEL) |
| prompts/ | 11-1~11-4 | 실측에 쓴 프롬프트 원문 |
| ai_generated_vague.pine | 11-1 | 모호한 프롬프트로 받은 AI 출력 (원본 그대로) |
| ai_generated_before.pine | 11-1 | 구조화된 프롬프트로 받은 AI 출력 (원본 그대로) |
| ai_verified_after.pine | 11-2 | 검토 후 수정한 지표 ([검토 수정] 주석) |
| ai_strategy_v1.pine | 11-3 | AI가 지표를 전략으로 바꾼 결과 |
| ai_strategy_v2.pine | 11-3 | AI 개선 결과 (수익률 계산 기준 오류 포함, 원본 그대로) |
| ai_strategy_v2_fixed.pine | 11-3 | 수익률 계산 기준을 고친 버전 |
| legacy_v5.pine | 11-4 | 변환 실습용 v5 전략 |
| ai_fix_v6.pine | 11-3, 11-4 | 컴파일 오류를 AI에 전달해 고친 v6 |
| tv_converted_v6.pine | 11-4 | TradingView 자동 변환 결과 |
| ai_converted_v6.pine | 11-4 | AI 변환 결과 (동작 동일 요구) |
