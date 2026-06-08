"""Prompt construction for real LLM calls."""

from __future__ import annotations


def build_prompt(code: str) -> str:
    return f"""你是一个面向编程初学者的代码解释助手。

任务要求：
1. 只解释用户提供的代码，不执行代码。
2. 使用中文回答，语气清晰、耐心、适合初学者。
3. 输出必须结构化，包含以下栏目：
   - 语言判断
   - 功能概述
   - 关键语句解释
   - 变量说明
   - 执行流程
   - 潜在问题
   - 优化建议
   - 学习提示
4. 如果代码存在 eval、exec、while True、裸 except、硬编码密码、文件写入等风险，请明确指出。

待解释代码：
```text
{code}
```
"""

