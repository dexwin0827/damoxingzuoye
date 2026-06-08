"""CLI entry point for the LLM Code Explainer Assistant."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from src.config import AppConfig
from src.llm_client import LLMClient
from src.prompt_builder import build_prompt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="基于大模型的代码解释助手")
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--code", help="直接传入待解释的代码")
    input_group.add_argument("--file", help="从文件读取待解释的代码")
    parser.add_argument("--mode", choices=["mock", "openai"], help="模型模式，默认读取 LLM_MODE 或 mock")
    parser.add_argument("--feedback-score", type=int, choices=range(1, 6), help="可选反馈评分，范围 1-5")
    parser.add_argument("--feedback-comment", default="", help="可选反馈文字，会保存到 outputs/feedback.jsonl")
    return parser.parse_args()


def read_code(args: argparse.Namespace) -> str:
    if args.code is not None:
        return args.code

    file_path = Path(args.file)
    if not file_path.exists():
        raise FileNotFoundError(f"代码文件不存在：{file_path}")
    if not file_path.is_file():
        raise ValueError(f"路径不是文件：{file_path}")
    return file_path.read_text(encoding="utf-8")


def save_feedback(code: str, explanation: str, score: int, comment: str) -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    payload = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "score": score,
        "comment": comment,
        "code_preview": code[:200],
        "explanation_preview": explanation[:300],
    }
    with (output_dir / "feedback.jsonl").open("a", encoding="utf-8") as file:
        file.write(json.dumps(payload, ensure_ascii=False) + "\n")


def main() -> int:
    args = parse_args()
    config = AppConfig.from_env(mode_override=args.mode)

    try:
        code = read_code(args).strip()
    except (OSError, ValueError) as exc:
        print(f"输入错误：{exc}", file=sys.stderr)
        return 1

    if not code:
        print("输入错误：代码内容不能为空。", file=sys.stderr)
        return 1

    prompt = build_prompt(code)
    client = LLMClient(config)
    explanation = client.explain_code(code=code, prompt=prompt)
    print(explanation)
    if args.feedback_score is not None:
        save_feedback(code, explanation, args.feedback_score, args.feedback_comment)
        print("\n反馈已保存到 outputs/feedback.jsonl")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
