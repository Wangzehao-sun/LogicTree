# LogicTree

[![tests](https://github.com/Wangzehao-sun/LogicTree/actions/workflows/tests.yml/badge.svg)](https://github.com/Wangzehao-sun/LogicTree/actions/workflows/tests.yml)

[English](README.md)

LogicTree 是一个合成逻辑推理数据生成框架。它先从目标结论反向构造符号逻辑树，再通过语言模型将符号规则转换为语义连贯的现实场景，最终生成选择题或长文本推理数据。

## 运行流程

```text
符号逻辑树
  → 规则、选项与推理链
  → 第一阶段语义转换
  → 解析模型输出
  → 构造选择题或故事提示词
  → 第二阶段推理生成
  → 答案校验与过滤
```

## 安装

项目要求 Python 3.10 或更高版本。

```bash
git clone https://github.com/Wangzehao-sun/LogicTree.git
cd LogicTree
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

## 配置模型接口

项目使用 OpenAI Chat Completions 兼容接口。运行模型阶段前，需要设置：

```bash
export LOGICTREE_API_URL='https://your-host.example/v1/chat/completions'
export LOGICTREE_API_KEY='your-api-key'
export LOGICTREE_MODEL='your-model-name'
```

请勿将真实 API 密钥提交到仓库。

## 完整示例

### 1. 生成并整理符号数据

```bash
logictree generate outputs/symbolic.jsonl \
  --counts 2:5,3:5 \
  --seed 42

logictree prepare-symbolic \
  outputs/symbolic.jsonl \
  outputs/prepared.jsonl
```

### 2. 将符号规则转换为现实场景

```bash
logictree stage1-prompts \
  outputs/prepared.jsonl \
  outputs/stage1-prompts.jsonl \
  --examples-per-tree 1 \
  --seed 42

logictree call-model \
  outputs/stage1-prompts.jsonl \
  --output-dir outputs/stage1-responses \
  --input-field prompt

logictree parse-stage1 \
  outputs/stage1-responses/stage1-prompts_success.jsonl \
  outputs/grounded.jsonl
```

### 3. 生成并过滤选择题推理数据

```bash
logictree choice-prompts \
  outputs/grounded.jsonl \
  outputs/choice-prompts.jsonl \
  --seed 42

logictree call-model \
  outputs/choice-prompts.jsonl \
  --output-dir outputs/choice-responses \
  --input-field instruction

logictree filter-choice \
  outputs/choice-responses/choice-prompts_success.jsonl \
  outputs/final-choice.jsonl
```

最终结果位于 `outputs/final-choice.jsonl`。

如需生成不同文体的长文本提示词，可使用：

```bash
logictree story-prompts outputs/grounded.jsonl outputs/story-prompts.jsonl --seed 42
```

对于一批已经整理好的符号 JSONL 文件，也可以直接运行：

```bash
./scripts/run_pipeline.sh data/input outputs
```
