"""자연어 요구사항을 보내 Pine Script 초안을 받는 예제 (11장).

사용법 (chapter11 폴더에서 실행):
    python ai_pine_request.py prompts/11-1_good.md my_result.pine

환경변수(현재 폴더 또는 예제 저장소 루트의 .env, 또는 셸):
    OPENAI_API_KEY   API 키
    OPENAI_MODEL     사용할 모델 이름
    OPENAI_BASE_URL  (선택) 기본값은 https://api.openai.com/v1
"""
import os
import re
import sys
from pathlib import Path

from openai import OpenAI

SYSTEM_PROMPT = (
    "당신은 TradingView Pine Script v6 전문가입니다. "
    "요청한 스크립트 전체를 ```pine 코드 블록 하나로만 답하고, "
    "코드 밖의 설명은 3줄 이내로 씁니다."
)


def load_dotenv(path: Path) -> None:
    """의존 패키지 없이 .env 파일의 KEY=VALUE를 환경변수로 읽는다."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def extract_pine(text: str) -> str:
    """응답에서 ```pine 코드 블록만 꺼낸다. 없으면 응답 전체를 돌려준다."""
    match = re.search(r"```(?:pine|pinescript)?\s*\n(.*?)```", text, re.S)
    return match.group(1).strip() + "\n" if match else text


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit("사용법: python ai_pine_request.py <프롬프트 파일> <저장할 .pine 파일>")
    load_dotenv(Path(".env"))
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")  # 예제 저장소 루트의 .env
    model = os.environ.get("OPENAI_MODEL")
    if not model:
        sys.exit("OPENAI_MODEL 환경변수를 설정하세요.")

    prompt = Path(sys.argv[1]).read_text(encoding="utf-8")
    client = OpenAI()  # OPENAI_API_KEY와 OPENAI_BASE_URL(선택)을 환경변수에서 읽는다
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    answer = response.choices[0].message.content or ""
    Path(sys.argv[2]).write_text(extract_pine(answer), encoding="utf-8")
    print(f"저장했습니다: {sys.argv[2]}")


if __name__ == "__main__":
    main()
