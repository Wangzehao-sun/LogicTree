"""Concurrent client for OpenAI-compatible chat-completions endpoints."""

from __future__ import annotations

import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import requests
from tqdm import tqdm

from .io import read_jsonl


@dataclass(frozen=True)
class ModelConfig:
    """Configuration for model inference over JSONL rows."""

    api_urls: Sequence[str]
    model: str
    api_key: Optional[str] = None
    max_tokens: int = 16_384
    temperature: float = 0.7
    top_p: float = 0.8
    timeout: float = 1_500
    retries: int = 10
    threads: int = 32
    stream: bool = False
    enable_thinking: bool = False
    extra_body: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.api_urls:
            raise ValueError("At least one API URL is required")
        if self.threads < 1:
            raise ValueError("threads must be at least 1")
        if self.retries < 0:
            raise ValueError("retries cannot be negative")


def _headers(config: ModelConfig) -> Dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if config.api_key:
        headers["Authorization"] = f"Bearer {config.api_key}"
    return headers


def _payload(prompt: str, config: ModelConfig, system_prompt: str = "") -> Dict[str, Any]:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload: Dict[str, Any] = {
        "model": config.model,
        "messages": messages,
        "max_tokens": config.max_tokens,
        "temperature": config.temperature,
        "top_p": config.top_p,
        "stream": config.stream,
        "chat_template_kwargs": {"enable_thinking": config.enable_thinking},
    }
    payload.update(config.extra_body)
    return payload


def _stream_text(response: requests.Response) -> str:
    chunks: List[str] = []
    for line in response.iter_lines():
        if not line:
            continue
        text = line.decode("utf-8").strip()
        if not text.startswith("data: "):
            continue
        data = text[6:]
        if data == "[DONE]":
            break
        event = json.loads(data)
        content = event.get("choices", [{}])[0].get("delta", {}).get("content", "")
        if content:
            chunks.append(content)
    return "".join(chunks)


def call_chat_completion(
    prompt: str,
    api_url: str,
    config: ModelConfig,
    *,
    system_prompt: str = "",
) -> str:
    """Call one chat-completions endpoint with bounded exponential backoff."""

    payload = _payload(prompt, config, system_prompt)
    for attempt in range(config.retries + 1):
        try:
            response = requests.post(
                api_url,
                headers=_headers(config),
                json=payload,
                timeout=config.timeout,
                stream=config.stream,
            )
            response.raise_for_status()
            if config.stream:
                return _stream_text(response)

            body = response.json()
            choices = body.get("choices", [])
            if not choices:
                raise ValueError("API response does not contain choices")
            return choices[0]["message"]["content"]
        except (requests.RequestException, ValueError, KeyError, json.JSONDecodeError):
            if attempt == config.retries:
                raise
            time.sleep(min(2**attempt * 0.1, 30))
    raise RuntimeError("Model request stopped unexpectedly")


def _process_row(
    index: int,
    row: Dict[str, Any],
    *,
    input_field: str,
    response_field: str,
    config: ModelConfig,
    system_prompt: str,
) -> Tuple[int, Dict[str, Any]]:
    prompt = row.get(input_field)
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError(f"Row {index + 1} has no non-empty '{input_field}' field")

    api_url = config.api_urls[index % len(config.api_urls)]
    response = call_chat_completion(prompt, api_url, config, system_prompt=system_prompt)
    result = dict(row)
    result[response_field] = response
    return index, result


def process_file(
    input_path: Path,
    output_dir: Path,
    config: ModelConfig,
    *,
    input_field: str,
    response_field: str = "model_answer",
    system_prompt: str = "",
) -> Dict[str, Any]:
    """Run model inference for one JSONL file and write success/error JSONL files."""

    rows = read_jsonl(input_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    success_path = output_dir / f"{input_path.stem}_success.jsonl"
    error_path = output_dir / f"{input_path.stem}_errors.jsonl"
    success_count = 0
    error_count = 0

    with success_path.open("w", encoding="utf-8") as success_file, error_path.open(
        "w", encoding="utf-8"
    ) as error_file:
        with ThreadPoolExecutor(max_workers=config.threads) as executor:
            futures = {
                executor.submit(
                    _process_row,
                    index,
                    row,
                    input_field=input_field,
                    response_field=response_field,
                    config=config,
                    system_prompt=system_prompt,
                ): (index, row)
                for index, row in enumerate(rows)
            }
            with tqdm(total=len(futures), desc=input_path.name, unit="row") as progress:
                for future in as_completed(futures):
                    index, original = futures[future]
                    try:
                        _, result = future.result()
                        success_file.write(json.dumps(result, ensure_ascii=False) + "\n")
                        success_count += 1
                    except Exception as error:  # preserve the failed input for recovery
                        failure = {
                            "file": str(input_path),
                            "line": index + 1,
                            "original": original,
                            "error": str(error),
                        }
                        error_file.write(json.dumps(failure, ensure_ascii=False) + "\n")
                        error_count += 1
                    progress.update(1)

    if error_count == 0:
        error_path.unlink()

    return {
        "input": str(input_path),
        "success_output": str(success_path),
        "error_output": str(error_path) if error_count else None,
        "total": len(rows),
        "success": success_count,
        "errors": error_count,
    }


def process_files(
    inputs: Iterable[Path],
    output_dir: Path,
    config: ModelConfig,
    **kwargs: Any,
) -> List[Dict[str, Any]]:
    """Run inference for multiple JSONL inputs."""

    return [process_file(path, output_dir, config, **kwargs) for path in inputs]
