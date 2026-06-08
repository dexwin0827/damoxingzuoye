"""Unified model client for mock and optional OpenAI modes."""

from __future__ import annotations

from .config import AppConfig
from .mock_llm import explain_with_mock


class LLMClient:
    def __init__(self, config: AppConfig):
        self.config = config

    def explain_code(self, code: str, prompt: str) -> str:
        if self.config.mode == "openai":
            return self._explain_with_openai(prompt)
        return explain_with_mock(code)

    def _explain_with_openai(self, prompt: str) -> str:
        if not self.config.openai_api_key:
            return (
                "OpenAI 模式未能启动：未检测到 OPENAI_API_KEY。\n"
                "请设置环境变量后重试，或使用默认 mock 模式运行。"
            )

        try:
            from openai import OpenAI  # type: ignore
        except Exception:
            return (
                "OpenAI 模式未能启动：当前环境未安装 openai SDK。\n"
                "本项目默认 mock 模式无需第三方依赖；如需真实 API，请安装 openai 包。"
            )

        try:
            client = OpenAI(api_key=self.config.openai_api_key)
            response = client.chat.completions.create(
                model=self.config.openai_model,
                messages=[
                    {"role": "system", "content": "你是一个中文代码解释助手。"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
            )
            content = response.choices[0].message.content
            return content or "OpenAI 返回了空内容，请稍后重试。"
        except Exception as exc:
            return f"OpenAI 调用失败：{exc}\n请检查网络、API Key、模型名称，或改用 mock 模式。"

