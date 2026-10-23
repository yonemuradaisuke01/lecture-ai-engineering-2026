"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

同じ質問を temperature 0.0 / 0.5 / 1.0 で実行し、各回答と実行時間を表示する。
ツールも会話履歴も持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse
from time import perf_counter

from google import genai
from google.genai import errors
from google.genai import types

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"
TEMPERATURES = (0.0, 0.5, 1.0)


def ask(question: str, temperature: float = 0.5) -> str:
    client = genai.Client(api_key=get_api_key())
    start = perf_counter()
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=question,
            config=types.GenerateContentConfig(temperature=temperature),
        )
    finally:
        print(f"[実行時間] {perf_counter() - start:.2f} 秒")

    usage = response.usage_metadata
    if usage is not None:
        print(
            f"[トークン] 入力: {usage.prompt_token_count}, "
            f"出力: {usage.candidates_token_count}"
        )

    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    print(f"[質問] {args.question}\n")
    had_api_error = False
    for temperature in TEMPERATURES:
        print(f"--- temperature: {temperature:.1f} ---")
        try:
            print(ask(args.question, temperature=temperature))
        except errors.APIError as e:
            print(api_error_message(e.code, e.message))
            had_api_error = True
        print()

    if had_api_error:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
