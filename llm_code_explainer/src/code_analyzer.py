"""Lightweight static code analysis for the mock explainer."""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class CodeAnalysis:
    language: str
    line_count: int
    features: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    variables: list[str] = field(default_factory=list)


def detect_language(code: str) -> str:
    lower_code = code.lower()
    if "std::" in code or "cout" in code or "cin" in code or "<iostream>" in code:
        return "C++"
    if "printf(" in code or "scanf(" in code or "<stdio.h>" in code:
        return "C"
    if re.search(r"\bint\s+main\s*\(", code):
        return "C"
    if re.search(r"\bdef\s+\w+\s*\(", code) or "print(" in code or "range(" in code:
        return "Python"
    if re.search(r"\b(class|for|while|if)\b", lower_code):
        return "Python 或类 C 语言"
    return "未知语言"


def _find_variables(code: str, language: str) -> list[str]:
    names: set[str] = set()
    if language.startswith("Python") or language == "未知语言":
        for match in re.finditer(r"^\s*([A-Za-z_]\w*)\s*=", code, re.MULTILINE):
            names.add(match.group(1))
        for match in re.finditer(r"\bfor\s+([A-Za-z_]\w*)\s+in\b", code):
            names.add(match.group(1))
    else:
        for match in re.finditer(r"\b(?:int|float|double|char|string|bool|long)\s+([A-Za-z_]\w*)", code):
            names.add(match.group(1))
    return sorted(names)


def analyze_code(code: str) -> CodeAnalysis:
    language = detect_language(code)
    lines = [line for line in code.splitlines() if line.strip()]
    features: list[str] = []
    risks: list[str] = []

    patterns = [
        ("包含输出语句", r"\bprint\s*\(|\bprintf\s*\(|\bcout\b"),
        ("包含输入语句", r"\binput\s*\(|\bscanf\s*\(|\bcin\b"),
        ("包含 for 循环", r"\bfor\b"),
        ("包含 while 循环", r"\bwhile\b"),
        ("包含条件判断", r"\bif\b|\belse\b|\belif\b"),
        ("包含函数定义", r"\bdef\s+\w+\s*\(|\b\w+\s+\w+\s*\([^;]*\)\s*\{"),
        ("包含类定义", r"\bclass\s+\w+"),
        ("包含列表或数组操作", r"\[[^\]]*\]|\bvector\s*<|\barray\b"),
        ("包含字典或映射结构", r"\{[^}]*:|dict\s*\(|\bmap\s*<"),
        ("包含排序逻辑", r"\bsorted\s*\(|\.sort\s*\(|\bsort\s*\("),
        ("包含异常处理", r"\btry\b|\bexcept\b|\bcatch\b"),
        ("包含文件读写", r"\bopen\s*\(|\bfopen\s*\(|\bifstream\b|\bofstream\b"),
        ("可能包含递归调用", r"\breturn\s+\w+\s*\([^)]*\)"),
    ]
    for label, pattern in patterns:
        if re.search(pattern, code):
            features.append(label)

    risk_patterns = [
        ("使用 eval，可能执行不可信字符串，存在安全风险", r"\beval\s*\("),
        ("使用 exec，可能执行动态代码，存在安全风险", r"\bexec\s*\("),
        ("存在 while True，需要确认循环内是否有可靠退出条件", r"\bwhile\s+True\s*:"),
        ("存在裸 except，可能掩盖真实错误原因", r"\bexcept\s*:"),
        ("代码中出现 password 字样，注意不要硬编码敏感信息", r"password"),
        ("存在文件写入操作，需要注意覆盖文件和权限问题", r"open\s*\([^)]*[\"']w[\"']|ofstream\b|fopen\s*\([^)]*[\"']w"),
    ]
    for label, pattern in risk_patterns:
        if re.search(pattern, code, re.IGNORECASE):
            risks.append(label)

    return CodeAnalysis(
        language=language,
        line_count=len(lines),
        features=features,
        risks=risks,
        variables=_find_variables(code, language),
    )
