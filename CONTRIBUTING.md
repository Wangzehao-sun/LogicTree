# Contributing

Thank you for improving LogicTree. Changes should preserve the distinction between symbolic correctness and model-generated language.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Pull requests

- Keep each change focused and explain its effect on the pipeline data contract.
- Add or update offline tests for symbolic rules, parsers, and output schemas.
- Use a fixed random seed in regression tests.
- Do not commit generated run directories, model caches, credentials, or private endpoint URLs.
- If a change alters a prompt, include a small before/after example and note possible dataset-distribution effects.
- Treat files under `scripts/legacy/` as historical provenance; implement supported behaviour in `src/logictree/`.

## Adding inference rules

New rules must be logically sound in the direction used by the forward reasoning trace. Add tests that verify both the generated premises and the recovered conclusion. If a rule changes sampling behaviour, document its weight and intended effect.

## Reporting bugs

Open an issue with the smallest reproducible input, Python version, command, seed, and traceback. Remove API keys and sensitive model inputs before posting.
