"""Parse and validate stage-one model responses."""

from __future__ import annotations

import json
import warnings


def _normalize_expression(expression):
    return str(expression).replace(" ", "").replace(".", "").replace(">", "→")


def process_generated_data_v1(data):
    """Validate grounded examples and retain fields needed by downstream stages."""

    processed = []
    for item in data:
        item_id = item.get("num", "unknown")
        example = item.get("example1")
        if not isinstance(example, dict):
            warnings.warn(f"Skipping item {item_id}: missing example1 object", stacklevel=2)
            continue
        if not all(key in example for key in ("propositions", "rules", "options")):
            warnings.warn(f"Skipping item {item_id}: incomplete grounded example", stacklevel=2)
            continue

        leaf_nodes = item.get("leaf_nodes", [])
        rules = example["rules"]
        options = example["options"]
        if not isinstance(rules, list) or len(rules) != len(leaf_nodes):
            warnings.warn(f"Skipping item {item_id}: rule count does not match leaves", stacklevel=2)
            continue
        if not isinstance(options, list) or not options:
            warnings.warn(f"Skipping item {item_id}: options must be a non-empty list", stacklevel=2)
            continue

        aligned = True
        for index, (leaf, rule) in enumerate(zip(leaf_nodes, rules), start=1):
            if not isinstance(rule, dict):
                aligned = False
                break
            expression = rule.get(f"rule{index}")
            if expression is None:
                expression = next((value for key, value in rule.items() if key.startswith("rule")), None)
            expected = _normalize_expression(leaf)
            actual = _normalize_expression(expression)
            if actual not in {expected, _normalize_expression(leaf[1:-1])}:
                aligned = False
                break
        if not aligned:
            warnings.warn(f"Skipping item {item_id}: grounded rules changed symbolic expressions", stacklevel=2)
            continue
        if not all(isinstance(rule.get("explanation"), str) for rule in rules):
            warnings.warn(f"Skipping item {item_id}: rule explanation is missing", stacklevel=2)
            continue
        if not all(isinstance(option.get("explanation"), str) for option in options):
            warnings.warn(f"Skipping item {item_id}: option explanation is missing", stacklevel=2)
            continue

        processed.append(
            {
                "num": item["num"],
                "step": item["step"],
                "logic_tree": item["logic_tree"],
                "leaf_nodes": leaf_nodes,
                "entities": example["propositions"],
                "rules": rules,
                "reasoning_steps": item["reasoning_steps"],
                "options": options,
            }
        )
    return processed


def merge_model_responses(data_list, response_field="model_answer"):
    """Extract embedded JSON objects and return validated grounded examples."""

    result = []
    for line in data_list:
        temp = line.get(response_field, "")
        index_start = temp.find('{')
        index_end = temp.rfind('}')
        target = temp
        if index_start != -1 and index_end >= index_start:
            target = temp[index_start:index_end+1]
        try:
            res = json.loads(target)
        except (TypeError, json.JSONDecodeError):
            continue
        new_line = line.copy()
        new_line.update(res)
        new_line.pop(response_field, None)
        result.append(new_line)
    return process_generated_data_v1(result)
