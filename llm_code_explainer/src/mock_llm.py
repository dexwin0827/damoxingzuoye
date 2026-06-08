"""Rule-based mock LLM used for offline course demonstration."""

from __future__ import annotations

import re

from .code_analyzer import analyze_code


def _overview(code: str, features: list[str]) -> str:
    if "可能包含递归调用" in features:
        return "这段代码通过函数自我调用解决重复子问题，属于递归思路。"
    if "包含排序逻辑" in features:
        return "这段代码主要用于对数据进行排序或展示排序结果。"
    if "包含类定义" in features:
        return "这段代码定义了类，用于把数据和相关行为组织在一起。"
    if "包含文件读写" in features:
        return "这段代码涉及文件读写，用于从文件获取数据或把结果保存到文件。"
    if "包含输入语句" in features:
        return "这段代码会读取用户输入，并根据输入继续处理。"
    if "包含 for 循环" in features or "包含 while 循环" in features:
        return "这段代码使用循环重复执行某些语句。"
    if "包含条件判断" in features:
        return "这段代码根据条件选择不同的执行分支。"
    if "包含输出语句" in features:
        return "这段代码主要向屏幕输出信息。"
    return "这段代码展示了基本的程序语句和数据处理过程。"


def _key_statements(code: str) -> list[str]:
    rules = [
        (r"\bprint\s*\(", "print(...)：在 Python 中用于向屏幕输出内容。"),
        (r"\bprintf\s*\(", "printf(...)：在 C 语言中用于格式化输出内容。"),
        (r"\bcout\b", "cout：在 C++ 中常用于向标准输出打印内容。"),
        (r"\binput\s*\(", "input(...)：读取用户在命令行输入的字符串。"),
        (r"\bfor\b", "for：用于按次数或按序列元素进行循环。"),
        (r"\bwhile\b", "while：只要条件成立就持续循环。"),
        (r"\bif\b", "if：用于条件判断，条件为真时执行对应代码块。"),
        (r"\bdef\s+\w+\s*\(", "def：定义 Python 函数，便于复用一段逻辑。"),
        (r"\bclass\s+\w+", "class：定义类，用于描述对象的数据和行为。"),
        (r"\bsorted\s*\(|\.sort\s*\(|\bsort\s*\(", "sort/sorted：用于对数据进行排序。"),
        (r"\btry\b|\bexcept\b", "try/except：用于捕获和处理运行时异常。"),
        (r"\bopen\s*\(|\bfopen\s*\(|\bifstream\b|\bofstream\b", "文件读写语句：用于读取或写入外部文件。"),
        (r"\beval\s*\(", "eval(...)：会把字符串当作代码执行，存在安全风险。"),
    ]
    explanations = [text for pattern, text in rules if re.search(pattern, code)]
    return explanations or ["代码由普通表达式或赋值语句组成，建议重点理解变量如何变化。"]


def _flow(features: list[str]) -> list[str]:
    steps = ["程序从第一条语句开始顺序执行。"]
    if "包含输入语句" in features:
        steps.append("读取用户输入，并把输入值保存到变量中。")
    if "包含条件判断" in features:
        steps.append("根据条件表达式选择不同分支。")
    if "包含 for 循环" in features or "包含 while 循环" in features:
        steps.append("进入循环后重复执行循环体，直到循环结束条件满足。")
    if "包含函数定义" in features:
        steps.append("函数定义本身不会立即执行，只有被调用时才运行函数体。")
    if "包含输出语句" in features:
        steps.append("最后通过输出语句把结果展示给用户。")
    return steps


def explain_with_mock(code: str) -> str:
    analysis = analyze_code(code)
    features = analysis.features
    risks = analysis.risks
    variables = analysis.variables

    feature_text = "、".join(features) if features else "未检测到明显的高级结构"
    variable_text = "、".join(variables) if variables else "未检测到明确变量，或变量不明显"
    risk_text = "\n".join(f"- {risk}" for risk in risks) if risks else "- 未发现明显高风险写法。"
    key_text = "\n".join(f"- {item}" for item in _key_statements(code))
    flow_text = "\n".join(f"{index}. {step}" for index, step in enumerate(_flow(features), start=1))

    suggestions = [
        "为关键步骤添加简短注释，帮助读者理解意图。",
        "给变量使用更具体的名称，避免含义模糊。",
    ]
    if risks:
        suggestions.append("优先修复潜在风险，尤其是动态执行代码、无限循环和文件写入问题。")
    if "包含函数定义" not in features and analysis.line_count > 6:
        suggestions.append("如果逻辑继续变长，可以考虑拆分成函数。")

    suggestion_text = "\n".join(f"- {item}" for item in suggestions)

    return f"""## 语言判断
{analysis.language}

## 功能概述
{_overview(code, features)}

## 关键语句解释
{key_text}

## 变量说明
{variable_text}

## 执行流程
{flow_text}

## 潜在问题
{risk_text}

## 优化建议
{suggestion_text}

## 学习提示
- 本例涉及的主要知识点：{feature_text}。
- 初学者可以先手动跟踪每一步变量值，再运行代码观察输出是否一致。
"""
