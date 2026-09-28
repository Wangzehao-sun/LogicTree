# LogicTree

[![tests](https://github.com/Wangzehao-sun/LogicTree/actions/workflows/tests.yml/badge.svg)](https://github.com/Wangzehao-sun/LogicTree/actions/workflows/tests.yml)

[简体中文](README.zh-CN.md)

LogicTree is a framework for generating synthetic logical-reasoning data. It constructs symbolic deduction trees backwards from a conclusion, uses a language model to ground the symbols in coherent real-world scenarios, and produces multiple-choice or long-form reasoning data.

## Pipeline

```text
Symbolic logic tree
  → rules, options, and reasoning trace
  → stage-one semantic grounding
  → model-output parsing
  → choice or story prompt construction
  → stage-two reasoning generation
  → answer validation and filtering
```

## Installation

LogicTree requires Python 3.10 or newer.

```bash
git clone https://github.com/Wangzehao-sun/LogicTree.git
cd LogicTree
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

## Model configuration

LogicTree uses an OpenAI-compatible Chat Completions endpoint. Configure it before running model stages:

```bash
export LOGICTREE_API_URL='https://your-host.example/v1/chat/completions'
export LOGICTREE_API_KEY='your-api-key'
export LOGICTREE_MODEL='your-model-name'
```

Never commit real API credentials.

## Complete example

### 1. Generate and prepare symbolic data

```bash
logictree generate outputs/symbolic.jsonl \
  --counts 2:5,3:5 \
  --seed 42

logictree prepare-symbolic \
  outputs/symbolic.jsonl \
  outputs/prepared.jsonl
```

### 2. Ground symbolic rules in real-world scenarios

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

### 3. Generate and filter multiple-choice reasoning data

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

The final dataset is written to `outputs/final-choice.jsonl`.

To build long-form prompts in different writing styles, use:

```bash
logictree story-prompts outputs/grounded.jsonl outputs/story-prompts.jsonl --seed 42
```

For a directory of prepared symbolic JSONL files, run the batch pipeline:

```bash
./scripts/run_pipeline.sh data/input outputs
```
