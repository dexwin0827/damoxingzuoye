# 基于大模型的代码解释助手实验报告

## 1. 实验题目

基于大模型的代码解释助手设计与评测。

## 2. 实验背景

随着大模型在自然语言理解和代码理解任务中的能力提升，将大模型用于辅助编程学习已经成为一种常见应用场景。对于编程初学者而言，阅读代码时常见困难包括：不理解语法结构、不清楚变量变化过程、无法判断程序执行流程、忽略潜在风险写法等。

本实验围绕“代码解释助手”场景，设计并实现一个小型大模型应用系统。系统支持用户输入 Python、C、C++ 代码，并输出中文结构化解释。考虑到课程作业的可验收性，系统默认使用 mock 模式，不依赖真实 API Key 和网络；同时保留 OpenAI API 模式，以体现真实大模型接口的接入方式。

在可选组件方面，系统采用结构化输出，并提供轻量用户反馈机制。反馈以 JSON Lines 文件保存，不引入数据库、RAG 或多 Agent，以控制复杂度。

## 3. 实验目的

本实验的主要目的如下：

1. 设计一个基于大模型思想的小型应用系统。
2. 实现一个可运行的代码解释助手原型。
3. 提供统一模型接口，支持 mock 模式和可选 OpenAI 模式。
4. 设计不少于 20 条用户输入样例，覆盖常见代码结构和风险点。
5. 通过批量测试生成系统输出和评测报告。
6. 分析系统优点、不足和后续改进方向。

## 4. 实验环境

实验环境如下：

| 项目 | 说明 |
| --- | --- |
| 操作系统 | Windows 环境 |
| 编程语言 | Python |
| 依赖库 | 默认 mock 模式仅使用 Python 标准库 |
| 运行方式 | 命令行 CLI |
| 默认模型 | mock 规则模型 |
| 可选模型 | OpenAI API，通过环境变量启用 |

默认实验不需要安装第三方依赖，不需要 API Key，也不需要联网。

## 5. 系统设计

### 5.1 总体架构

系统采用轻量分层架构：

```text
用户输入代码
    ↓
app.py 命令行入口
    ↓
prompt_builder.py 构造提示词
    ↓
llm_client.py 统一模型接口
    ├── mock_llm.py 离线规则解释
    └── OpenAI API 可选调用
    ↓
中文结构化解释
```

批量评测流程：

```text
run_tests.py
    ↓
evaluator.py
    ↓
读取 data/test_cases.json
    ↓
调用 mock 模式生成解释
    ↓
输出 outputs/test_results.json
    ↓
生成 reports/evaluation_report.md
```

### 5.2 模块说明

| 模块 | 作用 |
| --- | --- |
| `app.py` | 单条代码解释入口 |
| `run_tests.py` | 批量测试入口 |
| `src/config.py` | 读取运行模式和环境变量 |
| `src/code_analyzer.py` | 静态分析代码语言、结构和风险 |
| `src/mock_llm.py` | 根据规则生成中文结构化解释 |
| `src/llm_client.py` | 封装 mock 和 OpenAI 两种模型调用方式 |
| `src/prompt_builder.py` | 构造真实大模型提示词 |
| `src/evaluator.py` | 运行测试样例并生成评测报告 |

### 5.5 用户反馈机制

系统支持通过命令行参数保存用户反馈：

```powershell
python app.py --code "print('hello')" --feedback-score 5 --feedback-comment "解释清楚"
```

反馈记录保存到 `outputs/feedback.jsonl`。该机制用于展示“大模型应用系统”中常见的人机反馈闭环，但不引入数据库和登录功能，符合课程作业级原型定位。

### 5.3 输入输出设计

输入方式：

- 命令行直接输入代码：`python app.py --code "..."`
- 从文件读取代码：`python app.py --file sample.py`
- 批量读取测试样例：`python run_tests.py`

输出内容包含：

- 语言判断
- 功能概述
- 关键语句解释
- 变量说明
- 执行流程
- 潜在问题
- 优化建议
- 学习提示

### 5.4 模型调用设计

系统通过 `LLMClient` 统一模型调用方式。

mock 模式：

- 默认启用。
- 不访问网络。
- 不需要 API Key。
- 使用 `code_analyzer.py` 和 `mock_llm.py` 生成规则化解释。

OpenAI 模式：

- 通过 `LLM_MODE=openai` 启用。
- 通过 `OPENAI_API_KEY` 提供密钥。
- 通过 `OPENAI_MODEL` 指定模型名称。
- 缺少 API Key、SDK 或调用失败时返回友好错误信息。

## 6. 实验数据

实验使用 `data/test_cases.json` 中的 22 条测试样例。样例覆盖范围如下：

| 编号 | 类别 | 语言 |
| --- | --- | --- |
| TC001 | Hello world | Python |
| TC002 | 变量赋值 | Python |
| TC003 | 条件判断 | Python |
| TC004 | for 循环 | Python |
| TC005 | while 循环 | Python |
| TC006 | 函数 | Python |
| TC007 | 列表 | Python |
| TC008 | 字典 | Python |
| TC009 | 排序 | Python |
| TC010 | 递归 | Python |
| TC011 | 类 | Python |
| TC012 | 文件读取 | Python |
| TC013 | 文件写入 | Python |
| TC014 | 用户输入 | Python |
| TC015 | 异常处理 | Python |
| TC016 | eval 风险 | Python |
| TC017 | while True 风险 | Python |
| TC018 | C printf | C |
| TC019 | C++ cout | C++ |
| TC020 | 综合样例 | Python |
| TC021 | 裸 except 风险 | Python |
| TC022 | 敏感信息风险 | Python |

每条样例包含 `id`、`category`、`language`、`user_input`、`expected_focus` 和 `manual_score` 字段。

## 7. 实验步骤

### 7.1 单条样例运行

执行命令：

```powershell
python app.py --code "for i in range(3): print(i)"
```

系统输出：

```text
## 语言判断
Python

## 功能概述
这段代码使用循环重复执行某些语句。

## 关键语句解释
- print(...)：在 Python 中用于向屏幕输出内容。
- for：用于按次数或按序列元素进行循环。

## 变量说明
i

## 执行流程
1. 程序从第一条语句开始顺序执行。
2. 进入循环后重复执行循环体，直到循环结束条件满足。
3. 最后通过输出语句把结果展示给用户。

## 潜在问题
- 未发现明显高风险写法。
```

该结果说明系统能够正确识别 Python、for 循环、print 输出和循环变量。

### 7.2 批量测试运行

执行命令：

```powershell
python run_tests.py
```

系统输出：

```text
已完成 22 条样例测试。
测试结果：outputs/test_results.json
评测报告：reports/evaluation_report.md
```

批量测试会生成 JSON 格式的详细输出，并自动生成 Markdown 格式评测报告。

## 8. 评分标准

人工评分采用 1 到 5 分制，维度如下：

| 维度 | 含义 |
| --- | --- |
| completeness | 解释是否覆盖主要结构和功能 |
| clarity | 表达是否清楚，是否适合初学者 |
| usefulness | 是否有助于学习和修改代码 |
| risk_detection | 是否识别潜在风险 |
| overall | 综合评价 |

5 分表示表现最好，1 分表示表现较差。

## 9. 实验结果

根据 `outputs/test_results.json`，本次实验共运行 22 条测试样例。平均分如下：

| 维度 | 平均分 |
| --- | ---: |
| completeness | 4.73 |
| clarity | 4.82 |
| usefulness | 4.73 |
| risk_detection | 4.86 |
| overall | 4.77 |

从统计结果看，系统在清晰度和风险识别方面表现较好，说明固定结构化输出和规则风险检测对课程作业场景比较有效。

## 10. 典型案例分析

### 10.1 eval 风险样例

样例编号：TC016

输入代码：

```python
expr = input('expr: ')
print(eval(expr))
```

期望关注点：

- `eval`
- 安全风险
- 输入校验

分析结果：

系统能够识别 `input` 和 `eval`。其中 `eval` 会把字符串作为代码执行，如果用户输入不可信内容，可能造成安全风险。系统在“潜在问题”栏目中提示了该风险，并建议优先修复动态执行代码问题。

### 10.2 while True 风险样例

样例编号：TC017

输入代码：

```python
while True:
    command = input('> ')
    if command == 'quit':
        break
    print(command)
```

期望关注点：

- `while True`
- `break`
- 退出条件

分析结果：

系统识别出 while 循环、输入语句、条件判断和输出语句，并指出 `while True` 需要确认是否存在可靠退出条件。该样例虽然包含 `break`，但仍适合提醒初学者注意无限循环风险。

### 10.3 C printf 样例

样例编号：TC018

输入代码：

```c
#include <stdio.h>
int main() {
    printf("Hello C\n");
    return 0;
}
```

期望关注点：

- C 语言
- `printf`
- `main` 函数

分析结果：

系统能够判断该代码为 C 语言，并解释 `printf` 是 C 语言中的格式化输出函数。该样例验证了系统不仅支持 Python，也能覆盖基础 C 代码解释。

### 10.4 综合样例

样例编号：TC020

输入代码：

```python
def average(nums):
    total = 0
    for n in nums:
        total += n
    return total / len(nums)

scores = [80, 90, 100]
print(average(scores))
```

期望关注点：

- 函数
- 列表
- for 循环
- 平均值计算

分析结果：

系统能够识别函数定义、列表、for 循环和输出语句，并说明程序通过累加列表元素后除以长度得到平均值。该样例说明系统可以处理由多个基础结构组成的简单综合程序。

## 11. 实验结论

本实验完成了一个课程作业级的大模型代码解释助手原型。系统能够在默认 mock 模式下离线运行，并对 22 条测试样例生成中文结构化解释。测试结果表明，系统对常见语法结构、输入输出、循环、函数、类、文件读写和典型风险点具有较好的识别能力。

系统整体满足“大模型应用系统设计与评测”作业要求：

- 有明确应用场景。
- 有可运行原型。
- 有模型接口设计。
- 有 mock 模式和可选 OpenAI 模式。
- 有不少于 20 条测试样例。
- 有结构化输出和轻量用户反馈机制。
- 有系统设计文档、测试报告和实验报告。
- 有异常处理机制。
- 有批量评测输出。

## 12. 系统优点

- 默认 mock 模式无需 API Key，方便老师直接运行。
- 代码结构清晰，模块边界明确。
- 输出格式固定，便于初学者阅读。
- 支持 Python、C、C++ 的基础代码解释。
- 能识别 `eval`、`exec`、`while True`、裸 `except`、硬编码密码和文件写入等风险。
- 批量评测流程完整，能够生成测试结果和 Markdown 报告。

## 13. 系统不足

- mock 模式本质上是规则系统，无法完全替代真实大模型。
- 对复杂算法意图的理解有限，例如动态规划、图算法等。
- 对跨文件代码、第三方库调用和大型项目结构不支持。
- 语言判断基于启发式规则，极端情况下可能误判。
- 人工评分预先写在样例中，评测仍比较简单。

## 14. 改进方向

- 接入真实大模型，提高复杂代码解释能力。
- 增加更细粒度的测试集，例如错误代码、边界条件和复杂算法。
- 增加用户反馈字段，收集真实用户对解释质量的评价。
- 在不增加复杂度的前提下提供简单 Web 页面。
- 加强静态分析规则，例如检测除零风险、变量未定义风险和文件路径风险。

## 15. 实验心得

本实验说明，一个大模型应用系统不一定需要复杂前端、数据库或多 Agent 架构。对于课程作业而言，更重要的是明确应用场景、设计清晰的输入输出、封装模型调用接口、提供可运行原型，并通过测试样例形成评测闭环。

本项目通过 mock 模式解决了 API Key 和网络依赖问题，同时通过 OpenAI 模式保留了真实大模型接口扩展空间。这样的设计既降低了验收成本，也体现了大模型应用系统的核心结构。
