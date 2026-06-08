# 基于大模型的代码解释助手使用说明

## 1. 文档目的

本文档用于说明“基于大模型的代码解释助手”的安装、运行、测试、配置和常见问题处理方法。该系统是“大模型应用系统设计与评测”课程作业的可运行原型，默认采用 mock 模式，老师或同学无需 API Key、无需联网即可运行和验收。

## 2. 系统简介

本系统面向编程初学者或非计算机专业学生。用户输入一段 Python、C 或 C++ 代码，系统输出中文结构化解释，帮助用户理解代码的语言类型、主要功能、关键语句、变量含义、执行流程、潜在风险、优化建议和学习提示。

系统包含两种模型模式：

- `mock`：默认模式，基于规则生成解释，不需要网络和 API Key。
- `openai`：可选模式，通过 OpenAI API 调用真实大模型，需要环境变量配置。

## 3. 运行环境

推荐环境：

- 操作系统：Windows、macOS 或 Linux。
- Python：建议 Python 3.10 及以上。
- 第三方依赖：默认 mock 模式不需要第三方依赖。

检查 Python 是否可用：

```powershell
python --version
```

如果可以看到 Python 版本号，说明环境基本可用。

## 4. 项目结构说明

```text
llm_code_explainer/
├── README.md
├── requirements.txt
├── .env.example
├── app.py
├── run_tests.py
├── data/
│   └── test_cases.json
├── docs/
│   └── user_guide.md
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── llm_client.py
│   ├── mock_llm.py
│   ├── code_analyzer.py
│   ├── prompt_builder.py
│   └── evaluator.py
├── reports/
│   ├── system_design.md
│   ├── evaluation_report.md
│   └── experiment_report.md
└── outputs/
    ├── .gitkeep
    └── test_results.json
```

主要文件作用：

- `app.py`：命令行入口，用于解释单段代码。
- `run_tests.py`：批量测试入口，用于运行全部测试样例并生成报告。
- `src/config.py`：读取模型模式、API Key、模型名称等配置。
- `src/code_analyzer.py`：轻量静态分析，识别语言、结构和风险点。
- `src/mock_llm.py`：mock 模型，根据规则生成中文解释。
- `src/llm_client.py`：统一模型接口，负责选择 mock 或 OpenAI 模式。
- `src/prompt_builder.py`：构造真实大模型调用时使用的提示词。
- `src/evaluator.py`：批量评测逻辑，生成 JSON 结果和 Markdown 报告。
- `data/test_cases.json`：测试样例，共 22 条。
- `outputs/test_results.json`：批量测试输出结果。
- `reports/system_design.md`：系统设计文档。
- `reports/evaluation_report.md`：自动生成的测试报告。
- `reports/experiment_report.md`：实验报告。

## 5. 快速开始

进入项目目录：

```powershell
cd llm_code_explainer
```

运行一条代码解释：

```powershell
python app.py --code "for i in range(3): print(i)"
```

预期输出包含以下栏目：

```text
## 语言判断
Python

## 功能概述
...

## 关键语句解释
...

## 变量说明
...

## 执行流程
...

## 潜在问题
...

## 优化建议
...

## 学习提示
...
```

## 6. 单条代码解释

### 6.1 使用 `--code` 直接输入

适合解释较短代码：

```powershell
python app.py --code "print('Hello, world!')"
```

解释循环代码：

```powershell
python app.py --code "for i in range(5): print(i)"
```

解释函数代码：

```powershell
python app.py --code "def add(a, b): return a + b"
```

### 6.2 使用 `--file` 从文件读取

如果代码较长，建议先保存为文件，再用 `--file` 读取：

```powershell
python app.py --file sample.py
```

文件需要是文本代码文件。若文件不存在，系统会提示“代码文件不存在”，不会直接崩溃。

### 6.3 指定模型模式

默认使用 mock 模式。也可以显式指定：

```powershell
python app.py --mode mock --code "print('hello')"
```

OpenAI 模式：

```powershell
python app.py --mode openai --code "print('hello')"
```

若未配置 API Key，系统会返回友好提示。

## 7. 批量测试与报告生成

运行全部测试样例：

```powershell
python run_tests.py
```

运行后生成两个文件：

- `outputs/test_results.json`：保存每条样例的输入、评分和系统输出。
- `reports/evaluation_report.md`：自动生成测试报告。

测试样例来自：

```text
data/test_cases.json
```

当前样例数量为 22 条，覆盖：

- Hello world
- 变量赋值
- if 条件判断
- for 循环
- while 循环
- 函数
- 列表
- 字典
- 排序
- 递归
- 类
- 文件读取
- 文件写入
- input
- try/except
- eval 风险
- while True 风险
- C printf
- C++ cout
- 综合样例
- 裸 except 风险
- password 敏感信息风险

## 8. 用户反馈机制

系统提供一个可选的轻量反馈机制。用户可以在查看解释结果后，通过命令行参数保存评分和文字反馈：

```powershell
python app.py --code "print('hello')" --feedback-score 5 --feedback-comment "解释清楚，适合初学者"
```

参数说明：

- `--feedback-score`：1 到 5 分。
- `--feedback-comment`：用户对解释结果的文字评价。

反馈会追加写入：

```text
outputs/feedback.jsonl
```

该文件采用 JSON Lines 格式，每行是一条反馈记录。为了保持项目简单，系统没有引入数据库，也没有做用户登录。

## 9. OpenAI 模式配置

默认作业验收不需要 OpenAI API。若希望使用真实大模型，可以参考 `.env.example` 配置环境变量。

PowerShell 示例：

```powershell
$env:LLM_MODE="openai"
$env:OPENAI_API_KEY="your_api_key_here"
$env:OPENAI_MODEL="gpt-4o-mini"
python app.py --code "def add(a, b): return a + b"
```

环境变量说明：

- `LLM_MODE`：模型模式，可取 `mock` 或 `openai`。
- `OPENAI_API_KEY`：OpenAI API Key。
- `OPENAI_MODEL`：OpenAI 模型名称，默认示例为 `gpt-4o-mini`。

注意事项：

- mock 模式不需要安装 `openai` 包。
- openai 模式需要安装 OpenAI SDK。
- 如果 SDK 缺失、API Key 缺失或调用失败，程序会输出错误说明，不会中断整个系统。

## 10. 输出字段解释

系统输出采用固定结构：

| 字段 | 含义 |
| --- | --- |
| 语言判断 | 判断代码属于 Python、C、C++ 或未知语言 |
| 功能概述 | 用一两句话说明代码整体作用 |
| 关键语句解释 | 解释 print、for、while、if、函数、类等关键结构 |
| 变量说明 | 列出检测到的主要变量 |
| 执行流程 | 按顺序描述代码运行逻辑 |
| 潜在问题 | 提醒 eval、exec、while True、裸 except、文件写入等风险 |
| 优化建议 | 给出可读性、安全性或结构上的改进建议 |
| 学习提示 | 总结适合初学者关注的知识点 |

## 11. 常见错误与处理

### 10.1 代码为空

错误示例：

```powershell
python app.py --code ""
```

处理方式：传入非空代码。

### 10.2 文件不存在

错误示例：

```powershell
python app.py --file not_exist.py
```

处理方式：检查文件路径是否正确。

### 10.3 OpenAI API Key 缺失

错误示例：

```powershell
$env:LLM_MODE="openai"
python app.py --code "print('hello')"
```

处理方式：设置 `OPENAI_API_KEY`，或改回默认 mock 模式。

### 10.4 PowerShell 中文显示乱码

如果使用 `Get-Content` 查看 Markdown 时中文显示乱码，通常是控制台编码显示问题，文件本身仍为 UTF-8。可以直接用编辑器打开 Markdown 文件，或在支持 UTF-8 的终端中查看。

## 12. 验收建议

课程验收时建议依次执行：

```powershell
cd llm_code_explainer
python app.py --code "for i in range(3): print(i)"
python run_tests.py
```

然后检查：

- 命令行是否输出中文结构化解释。
- `outputs/test_results.json` 是否生成。
- `reports/evaluation_report.md` 是否生成。
- `reports/system_design.md` 是否内容完整。
- `reports/experiment_report.md` 是否说明实验过程和结果。

## 13. 使用边界

本项目是课程作业级原型，不是生产级系统。它适合演示大模型应用系统的基本流程、mock 模型接口、异常处理和评测闭环；不适合替代专业代码审查、安全审计或大型 IDE 插件。
