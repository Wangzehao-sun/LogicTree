# Architecture

## Design goals

LogicTree separates deterministic symbolic construction from non-deterministic language-model generation. This boundary makes the logical source of truth inspectable, permits offline testing, and allows different model providers to be compared without changing the generator.

## Pipeline stages

1. **Symbolic generation** (`core.py`) starts from a sampled conclusion and expands leaves into sufficient premises.
2. **Symbolic preparation** converts leaves into numbered rules, turns internal nodes into positive and contradictory options, and renders the deduction path as text.
3. **Semantic grounding** (`prompts/stage1.py`) asks a model to map symbols to events in one coherent domain while preserving every expression.
4. **Grounding validation** (`processing/stage1.py`) extracts the model's JSON object, checks required sections, and aligns generated rules with the original leaves.
5. **Task construction** creates either shuffled multiple-choice prompts (`prompts/choice.py`) or style-conditioned long-form prompts (`prompts/story.py`).
6. **Inference** (`model.py`) calls one or more OpenAI-compatible endpoints concurrently and records failed rows separately.
7. **Filtering** (`processing/choice.py`) normalizes the final `\boxed{}` answer and retains only label-consistent records.

## Symbolic representation

`LogicTreeNode` stores a normalized expression in `value` and up to three premise children (`left`, `mid`, and `right`). A leaf is an initial premise; an internal node is a derived conclusion. `LogicTree.split_order` records expansions, and its reverse is therefore the forward reasoning sequence.

The generator currently uses these symbol forms:

| Symbol | Meaning |
| --- | --- |
| `~P` | negation |
| `P & Q` | conjunction |
| `P \| Q` | inclusive disjunction |
| `P → Q` or `P > Q` | implication |
| `P ⊕ Q` | exclusive disjunction in legacy expressions |
| `∀x(...)` | limited universal-rule templates |

Representative backward-expansion templates include:

- `P → Q`, `P` ⟹ `Q` (modus ponens)
- `P ∨ Q`, `¬P` ⟹ `Q` (disjunctive syllogism)
- `P → R`, `R → Q` ⟹ `P → Q` (hypothetical syllogism)
- `P → Q`, `¬Q` ⟹ `¬P` (modus tollens)
- `¬(¬P ∧ ¬Q)` ⟹ `P ∨ Q` (De Morgan equivalence)

The first-order mode adds a small set of universally quantified templates over a single constant `a`; it is not a general first-order theorem prover.

## Data contracts

All persisted pipeline data uses UTF-8 JSONL. Each stage preserves `num`, the stable example identifier, whenever it is present.

- **Raw symbolic:** `step`, `logic_tree`, `leaf_nodes`, `inodes`, `reasoning_process`, `num`.
- **Prepared symbolic:** raw fields plus `rules`, `reasoning_steps`, `options`, and `conclusion`.
- **Grounding prompt:** prepared fields plus `prompt` and sampled `domain` values.
- **Grounded record:** symbolic metadata plus `entities`, model-generated `rules`, and model-generated `options`.
- **Choice prompt:** `num`, `context`, labeled `options`, expected `answer`, and `instruction`.
- **Model result:** input record plus the configured response field (default `model_answer`).

## Extension points

- Add a sound local expansion rule as a `LogicTreeNode` method and include it in `_split` with an explicit sampling weight.
- Add a task format under `prompts/` and expose it through `cli.py`.
- Adapt a non-compatible provider behind `call_chat_completion` while keeping the JSONL inference contract.
- Add stricter semantic validators after `merge_model_responses`; symbolic correctness alone does not guarantee faithful natural-language grounding.

## Known limitations

- Expression parsing is intentionally lightweight and does not implement a full precedence-aware formal grammar.
- Duplicate detection compares tree structures linearly and can become expensive on very large generations.
- Some rule selection probabilities are inherited research parameters rather than calibrated distributions.
- Long prompt examples materially increase token usage.
- Historical notebooks and files in `scripts/legacy/` are provenance artifacts, not the supported public API.
