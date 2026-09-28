"""Command-line interface for the LogicTree data-generation pipeline."""

from __future__ import annotations

import argparse
import json
import os
from importlib.resources import as_file, files
from pathlib import Path
from typing import Dict, Sequence

from . import __version__
from .core import DEFAULT_STEP_COUNTS, generate_dataset, process_data
from .io import read_jsonl, save_jsonl
from .processing.choice import process_jsonl_file as filter_choice_file
from .processing.stage1 import merge_model_responses
from .processing.story import process_jsonl_file as filter_story_file
from .prompts.choice import generate_choice_train_data, generate_question
from .prompts.stage1 import generate_data_with_llm_v1_prompts, merge_all_domains_to_list
from .prompts.story import generate_reasoning_prompt, prepare_data


def _parse_counts(value: str) -> Dict[int, int]:
    try:
        result = {}
        for pair in value.split(","):
            step, count = pair.split(":", maxsplit=1)
            result[int(step)] = int(count)
        return result
    except ValueError as error:
        raise argparse.ArgumentTypeError("Use STEP:COUNT pairs, e.g. 2:10,3:20") from error


def _add_io(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("input", type=Path, help="Input JSONL file")
    parser.add_argument("output", type=Path, help="Output JSONL file")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="logictree",
        description="Generate and ground synthetic logical-reasoning datasets.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    generate = commands.add_parser("generate", help="Generate symbolic logic trees")
    generate.add_argument("output", type=Path)
    generate.add_argument(
        "--counts",
        type=_parse_counts,
        default=DEFAULT_STEP_COUNTS,
        help="Comma-separated STEP:COUNT pairs (default: research distribution)",
    )
    generate.add_argument("--existing", type=Path, help="Optional corpus used for deduplication")
    generate.add_argument("--first-order", action="store_true")
    generate.add_argument("--seed", type=int)

    prepare = commands.add_parser("prepare-symbolic", help="Add rules, options, and reasoning text")
    _add_io(prepare)

    stage1 = commands.add_parser("stage1-prompts", help="Build semantic-grounding prompts")
    _add_io(stage1)
    stage1.add_argument(
        "--domains",
        type=Path,
        help="Domain taxonomy JSON (default: packaged taxonomy)",
    )
    stage1.add_argument("--examples-per-tree", type=int, default=10)
    stage1.add_argument("--seed", type=int)

    parse_stage1 = commands.add_parser("parse-stage1", help="Parse grounded model responses")
    _add_io(parse_stage1)
    parse_stage1.add_argument("--response-field", default="model_answer")

    choices = commands.add_parser("choice-prompts", help="Build multiple-choice prompts")
    _add_io(choices)
    choices.add_argument("--seed", type=int)

    stories = commands.add_parser("story-prompts", help="Build style-conditioned story prompts")
    _add_io(stories)
    stories.add_argument("--seed", type=int)

    model = commands.add_parser("call-model", help="Call an OpenAI-compatible model endpoint")
    model.add_argument("inputs", type=Path, nargs="+")
    model.add_argument("--output-dir", type=Path, required=True)
    model.add_argument("--input-field", required=True)
    model.add_argument("--response-field", default="model_answer")
    model.add_argument("--api-url", action="append")
    model.add_argument("--model", default=os.getenv("LOGICTREE_MODEL", ""))
    model.add_argument("--api-key-env", default="LOGICTREE_API_KEY")
    model.add_argument("--threads", type=int, default=32)
    model.add_argument("--retries", type=int, default=10)
    model.add_argument("--timeout", type=float, default=1_500)
    model.add_argument("--max-tokens", type=int, default=16_384)
    model.add_argument("--temperature", type=float, default=0.7)
    model.add_argument("--top-p", type=float, default=0.8)
    model.add_argument("--stream", action="store_true")
    model.add_argument("--enable-thinking", action="store_true")
    model.add_argument("--system-prompt", default="")

    filter_choice = commands.add_parser("filter-choice", help="Keep responses with correct boxed answers")
    _add_io(filter_choice)
    filter_choice.add_argument("--expected-field", default="answer")
    filter_choice.add_argument("--response-field", default="model_answer")

    filter_story = commands.add_parser("filter-story", help="Filter long-form boxed answers")
    _add_io(filter_story)
    filter_story.add_argument("--expected-field", default="output")
    filter_story.add_argument("--response-field", default="model_answer")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "generate":
        existing = read_jsonl(args.existing) if args.existing else []
        rows = generate_dataset(
            args.counts,
            existing=existing,
            first_order=args.first_order,
            seed=args.seed,
        )
        save_jsonl(rows, args.output, "w")
    elif args.command == "prepare-symbolic":
        save_jsonl(process_data(read_jsonl(args.input)), args.output, "w")
    elif args.command == "stage1-prompts":
        if args.domains:
            domains = merge_all_domains_to_list(args.domains)
        else:
            packaged_domains = files("logictree.resources").joinpath("domain.json")
            with as_file(packaged_domains) as domain_path:
                domains = merge_all_domains_to_list(domain_path)
        rows = generate_data_with_llm_v1_prompts(
            read_jsonl(args.input),
            domains,
            examples_per_tree=args.examples_per_tree,
            seed=args.seed,
        )
        save_jsonl(rows, args.output, "w")
    elif args.command == "parse-stage1":
        rows = merge_model_responses(read_jsonl(args.input), args.response_field)
        save_jsonl(rows, args.output, "w")
    elif args.command == "choice-prompts":
        rows = generate_question(read_jsonl(args.input))
        save_jsonl(generate_choice_train_data(rows, seed=args.seed), args.output, "w")
    elif args.command == "story-prompts":
        rows = prepare_data(read_jsonl(args.input))
        save_jsonl(generate_reasoning_prompt(rows, seed=args.seed), args.output, "w")
    elif args.command == "call-model":
        from .model import ModelConfig, process_files

        api_urls = args.api_url or [url for url in os.getenv("LOGICTREE_API_URL", "").split(",") if url]
        if not api_urls:
            parser.error("call-model requires --api-url or LOGICTREE_API_URL")
        if not args.model:
            parser.error("call-model requires --model or LOGICTREE_MODEL")
        config = ModelConfig(
            api_urls=api_urls,
            model=args.model,
            api_key=os.getenv(args.api_key_env),
            max_tokens=args.max_tokens,
            temperature=args.temperature,
            top_p=args.top_p,
            timeout=args.timeout,
            retries=args.retries,
            threads=args.threads,
            stream=args.stream,
            enable_thinking=args.enable_thinking,
        )
        reports = process_files(
            args.inputs,
            args.output_dir,
            config,
            input_field=args.input_field,
            response_field=args.response_field,
            system_prompt=args.system_prompt,
        )
        print(json.dumps(reports, ensure_ascii=False, indent=2))
    elif args.command == "filter-choice":
        args.output.parent.mkdir(parents=True, exist_ok=True)
        filter_choice_file(
            args.input,
            args.output,
            expected_field=args.expected_field,
            response_field=args.response_field,
        )
    elif args.command == "filter-story":
        args.output.parent.mkdir(parents=True, exist_ok=True)
        filter_story_file(
            args.input,
            args.output,
            expected_field=args.expected_field,
            response_field=args.response_field,
        )
    return 0
