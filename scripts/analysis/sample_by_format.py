"""Sample a bounded number of records from each story format."""

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path


def sample_by_format(input_path, output_dir, count=500, seed=None):
    if seed is not None:
        random.seed(seed)

    groups = defaultdict(list)
    with Path(input_path).open("r", encoding="utf-8") as source:
        for line_number, line in enumerate(source, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"Invalid JSON at line {line_number}: {error.msg}") from error
            groups[row.get("format", "unknown")].append(row)

    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    for output_format, rows in sorted(groups.items()):
        chosen = random.sample(rows, min(count, len(rows)))
        with (target / f"{output_format}.jsonl").open("w", encoding="utf-8") as output:
            for row in chosen:
                output.write(json.dumps(row, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    parser.add_argument("output_dir")
    parser.add_argument("--count", type=int, default=500)
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()
    sample_by_format(args.input, args.output_dir, args.count, args.seed)
