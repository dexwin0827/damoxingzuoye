"""Batch evaluation utilities."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Any

from .config import AppConfig
from .llm_client import LLMClient
from .prompt_builder import build_prompt


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "data" / "test_cases.json"
OUTPUT_PATH = ROOT / "outputs" / "test_results.json"
REPORT_PATH = ROOT / "reports" / "evaluation_report.md"


def _load_cases() -> list[dict[str, Any]]:
    with CASES_PATH.open("r", encoding="utf-8") as file:
        cases = json.load(file)
    if not isinstance(cases, list):
        raise ValueError("test_cases.json 必须是列表。")
    return cases


def _score_stats(cases: list[dict[str, Any]]) -> dict[str, float]:
    dimensions = ["completeness", "clarity", "usefulness", "risk_detection", "overall"]
    stats: dict[str, float] = {}
    for dimension in dimensions:
        values = [
            case.get("manual_score", {}).get(dimension)
            for case in cases
            if isinstance(case.get("manual_score", {}).get(dimension), (int, float))
        ]
        stats[dimension] = round(mean(values), 2) if values else 0.0
    return stats


def _shorten(text: str, limit: int = 80) -> str:
    one_line = " ".join(text.split())
    return one_line[: limit - 3] + "..." if len(one_line) > limit else one_line


def _build_report(results: list[dict[str, Any]], stats: dict[str, float]) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines: list[str] = [
        "# 代码解释助手测试报告",
        "",
        f"生成时间：{generated_at}",
        "",
        "## 1. 测试目的",
        "",
        "验证系统在 mock 模式下是否能够对 Python、C、C++ 代码生成中文结构化解释，并检查风险识别、清晰度和实用性是否满足课程作业要求。",
        "",
        "## 2. 测试方法",
        "",
        "使用 `data/test_cases.json` 中的测试样例批量调用系统。每条样例包含用户输入、期望关注点和人工评分。运行 `python run_tests.py` 后，系统输出保存到 `outputs/test_results.json`，本报告自动生成。",
        "",
        "## 3. 评分标准",
        "",
        "- completeness：解释是否覆盖主要结构和功能。",
        "- clarity：表达是否清楚，是否适合初学者。",
        "- usefulness：解释是否有助于学习和修改代码。",
        "- risk_detection：是否识别潜在风险。",
        "- overall：综合评价。",
        "",
        "评分范围为 1 到 5 分，5 分最好。",
        "",
        "## 4. 统计结果",
        "",
        "| 维度 | 平均分 |",
        "| --- | ---: |",
    ]
    for key, value in stats.items():
        lines.append(f"| {key} | {value} |")

    lines.extend([
        "",
        "## 5. 测试样例表",
        "",
        "| ID | 类别 | 语言 | 期望关注点 | 综合分 | 输出摘要 |",
        "| --- | --- | --- | --- | ---: | --- |",
    ])
    for result in results:
        case = result["case"]
        score = case["manual_score"]["overall"]
        output_summary = _shorten(result["output"].replace("|", "/"))
        focus = "、".join(case["expected_focus"]).replace("|", "/")
        lines.append(
            f"| {case['id']} | {case['category']} | {case['language']} | {focus} | {score} | {output_summary} |"
        )

    typical_ids = ["TC016", "TC017", "TC020"]
    lines.extend(["", "## 6. 典型案例分析", ""])
    for typical_id in typical_ids:
        matched = next((item for item in results if item["case"]["id"] == typical_id), None)
        if not matched:
            continue
        case = matched["case"]
        lines.extend([
            f"### {case['id']}：{case['category']}",
            "",
            f"- 输入摘要：`{_shorten(case['user_input'], 100)}`",
            f"- 期望关注点：{'、'.join(case['expected_focus'])}",
            f"- 系统输出摘要：{_shorten(matched['output'], 160)}",
            f"- 人工综合评分：{case['manual_score']['overall']}",
            "",
        ])

    lines.extend([
        "## 7. 系统优点",
        "",
        "- 默认 mock 模式可离线运行，降低课堂验收门槛。",
        "- 输出结构固定，便于阅读和比较不同样例。",
        "- 能识别常见语法结构和部分安全风险，如 eval、while True、文件写入和裸 except。",
        "- 代码量少，主要依赖 Python 标准库，便于理解和提交。",
        "",
        "## 8. 系统不足",
        "",
        "- mock 模式基于规则，无法像真实大模型一样理解复杂上下文。",
        "- 递归、变量用途和算法意图的判断较粗略。",
        "- 人工评分写在测试样例中，不能替代严格的自动化质量评估。",
        "",
        "## 9. 改进方向",
        "",
        "- 接入真实大模型后提升复杂代码解释质量。",
        "- 增加更多语言和更多错误类型识别。",
        "- 引入更细粒度的人工评测表，例如按每个输出栏目单独评分。",
    ])
    return "\n".join(lines) + "\n"


def run_evaluation() -> None:
    cases = _load_cases()
    config = AppConfig(mode="mock")
    client = LLMClient(config)
    results: list[dict[str, Any]] = []

    for case in cases:
        code = case["user_input"]
        output = client.explain_code(code=code, prompt=build_prompt(code))
        results.append({"case": case, "output": output})

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "mock",
        "case_count": len(cases),
        "score_stats": _score_stats(cases),
        "results": results,
    }
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    REPORT_PATH.write_text(_build_report(results, payload["score_stats"]), encoding="utf-8")

    print(f"已完成 {len(cases)} 条样例测试。")
    print(f"测试结果：{OUTPUT_PATH}")
    print(f"评测报告：{REPORT_PATH}")

