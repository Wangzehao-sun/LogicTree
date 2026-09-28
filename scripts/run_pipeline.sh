#!/usr/bin/env bash
set -euo pipefail

# End-to-end choice-data pipeline for an input directory of prepared symbolic
# JSONL files. Configure the model endpoint with LOGICTREE_API_URL,
# LOGICTREE_API_KEY, and LOGICTREE_MODEL before running this script.

input_dir="${1:-data/input}"
work_dir="${2:-outputs}"

if [[ ! -d "$input_dir" ]]; then
  echo "Input directory does not exist: $input_dir" >&2
  exit 1
fi

mkdir -p \
  "$work_dir/stage1-prompts" \
  "$work_dir/stage1-responses" \
  "$work_dir/grounded" \
  "$work_dir/choice-prompts" \
  "$work_dir/choice-responses" \
  "$work_dir/final"

stage1_prompts=()
while IFS= read -r source_file; do
  stem="$(basename "$source_file" .jsonl)"
  prompt_file="$work_dir/stage1-prompts/${stem}.jsonl"
  logictree stage1-prompts "$source_file" "$prompt_file"
  stage1_prompts+=("$prompt_file")
done < <(find "$input_dir" -maxdepth 1 -type f -name '*.jsonl' | sort)

if [[ ${#stage1_prompts[@]} -eq 0 ]]; then
  echo "No JSONL files found in: $input_dir" >&2
  exit 1
fi

logictree call-model \
  "${stage1_prompts[@]}" \
  --output-dir "$work_dir/stage1-responses" \
  --input-field prompt

choice_prompts=()
for prompt_file in "${stage1_prompts[@]}"; do
  stem="$(basename "$prompt_file" .jsonl)"
  response_file="$work_dir/stage1-responses/${stem}_success.jsonl"
  grounded_file="$work_dir/grounded/${stem}.jsonl"
  choice_file="$work_dir/choice-prompts/${stem}.jsonl"
  logictree parse-stage1 "$response_file" "$grounded_file"
  logictree choice-prompts "$grounded_file" "$choice_file"
  choice_prompts+=("$choice_file")
done

logictree call-model \
  "${choice_prompts[@]}" \
  --output-dir "$work_dir/choice-responses" \
  --input-field instruction

for choice_file in "${choice_prompts[@]}"; do
  stem="$(basename "$choice_file" .jsonl)"
  response_file="$work_dir/choice-responses/${stem}_success.jsonl"
  logictree filter-choice "$response_file" "$work_dir/final/${stem}.jsonl"
done

echo "Pipeline complete. Final datasets: $work_dir/final"
