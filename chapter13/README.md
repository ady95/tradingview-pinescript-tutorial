# 13장. Claude Code와 TradingView MCP

Claude Code에 TradingView 공식 MCP 서버(베타)를 연결해 시세 조회·Pine Script 검증·백테스트를 자동화하는 예제입니다.

필요한 것: Claude Code(Claude 유료 요금제), TradingView Essential 이상 요금제(체험판 불가).

| 파일 | 내용 | 절 |
|---|---|---|
| `.claude/settings.json` | TradingView MCP의 쓰기 도구 12개(스크립트 저장, 알림·관심종목 변경)를 막는 설정. 이 폴더에서 Claude Code를 실행하면 적용됩니다 | 13-1 |
| `prompts/13-2_screen.md` | 스크리너로 후보를 넓게 거른 뒤 07-3 지표 코드로 네 조건을 판정하는 요청 예시 | 13-2 |
| `CLAUDE.md` | Claude Code가 이 폴더에서 자동으로 읽는 작업 규칙 (검증 → 백테스트 순서, 결과 보고 형식) | 13-3 |
| `prompts/13-3_strategy.md` | 11-3과 같은 요구사항으로 전략 작성·검증·백테스트를 요청하는 예시 | 13-3 |
| `strategy_rsi_bb.pine` | 위 요청으로 Claude Code가 만든 전략 (실측 결과 그대로, 수정하지 않음) | 13-3 |
| `paper_mcp/server.py` | 12장 모의매매 서버의 감사 로그·키움 모의투자 잔고를 읽기 전용 도구로 제공하는 MCP 서버 (주문 도구 없음) | 13-4 |
| `paper_mcp/requirements.txt` | 위 서버에 필요한 패키지 (`mcp` 2.x, `httpx`) | 13-4 |

서버 등록 (모든 폴더에서 사용):

```bash
claude mcp add --transport http --scope user mcp-tradingview https://mcp.tradingview.com/mcp
```

등록 후 Claude Code를 다시 실행하고 `/mcp`에서 TradingView 계정으로 로그인합니다.

TradingView MCP는 공개 베타라 도구 목록과 동작이 바뀔 수 있습니다. 이 폴더의 결과는 2026-11-14 실측 기준입니다.
