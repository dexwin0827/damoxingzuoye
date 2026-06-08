# 基于大模型的代码解释助手

本项目对应课程作业“大模型应用系统设计与评测”，实现一个面向编程初学者的轻量级代码解释助手。用户输入 Python、C 或 C++ 代码后，系统输出中文结构化解释，包括语言判断、功能概述、关键语句解释、变量说明、执行流程、潜在问题、优化建议和学习提示。

项目默认使用 mock 模式，不需要 API Key、不访问网络，老师拿到后可以直接运行。也可以通过环境变量启用 OpenAI API 模式，但这不是默认要求。

## 项目结构

```text
llm_code_explainer/
├── README.md
├── requirements.txt
├── .env.example
├── app.py
├── run_tests.py
├── data/test_cases.json
├── src/__init__.py
├── src/config.py
├── src/llm_client.py
├── src/mock_llm.py
├── src/code_analyzer.py
├── src/prompt_builder.py
├── src/evaluator.py
├── reports/system_design.md
├── reports/evaluation_report.md
└── outputs/.gitkeep
```

## 运行方法

直接输入代码：

```powershell
python app.py --code "for i in range(3): print(i)"
```

从文件读取代码：

```powershell
python app.py --file path\to\sample.py
```

指定 mock 模式：

```powershell
python app.py --mode mock --code "print('hello')"
```

可选保存用户反馈：

```powershell
python app.py --code "print('hello')" --feedback-score 5 --feedback-comment "解释清楚"
```

反馈会追加保存到 `outputs/feedback.jsonl`，用于展示简单的用户反馈机制。

## 批量测试

运行全部测试样例并生成报告：

```powershell
python run_tests.py
```

运行后会生成：

- `outputs/test_results.json`
- `reports/evaluation_report.md`

## 详细文档

- [详细使用说明](docs/user_guide.md)
- [系统设计文档](reports/system_design.md)
- [测试报告](reports/evaluation_report.md)
- [实验报告](reports/experiment_report.md)

本项目采用结构化输出作为可选组件，并额外提供轻量用户反馈机制；未引入 RAG、多 Agent、数据库或复杂前端。

## mock 与 OpenAI 模式

默认模式为 mock：

```powershell
$env:LLM_MODE="mock"
```

可选启用 OpenAI：

```powershell
$env:LLM_MODE="openai"
$env:OPENAI_API_KEY="your_api_key_here"
$env:OPENAI_MODEL="gpt-4o-mini"
python app.py --code "def add(a, b): return a + b"
```

如果没有安装 OpenAI SDK、没有设置 API Key，或 API 调用失败，程序会返回友好错误信息，不会崩溃。

## 常见问题

**没有 API Key 能运行吗？**  
可以。项目默认 mock 模式，完全离线可运行。

**是否需要安装第三方依赖？**  
mock 模式不需要。`requirements.txt` 中也说明了这一点。

**系统会执行用户输入的代码吗？**  
不会。系统只做轻量静态分析和解释，不执行代码，避免安全风险。

**为什么不做 RAG、多 Agent 或数据库？**  
本项目定位是课程作业级原型，重点是系统设计、模型调用接口、异常处理和评测闭环。过度工程化会增加代码复杂度，不利于作业验收。
