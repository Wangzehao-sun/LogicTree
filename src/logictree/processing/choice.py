"""Filter multiple-choice model responses by their boxed final answer."""

from __future__ import annotations

import json
import re

def extract_boxed_answer_enhanced(response):
    """
    从回答中提取\\boxed{}中的答案，支持嵌套括号，并增强了对选择题选项的清洗能力。
    """
    if not response:
        return None

    # --- 核心提取逻辑 (保持不变，这部分写得很好) ---
    boxed_positions = []
    i = 0
    while i < len(response):
        if response[i:i+7] == '\\boxed{':
            boxed_positions.append(i + 7)
        i += 1
    
    # 兜底策略：如果没有 \boxed{}
    if not boxed_positions:
        # 扩展了正则，支持浮点数、分数等，不仅仅是 \d+
        answer_patterns = [
            r'(?:the|our|final|my)?\s*(?:answer|result|value)(?:\s+is)?\s*(?:=|:)?\s*([0-9a-zA-Z\.\/\+\-]+)',
            r'(?:=|:)\s*([0-9a-zA-Z\.\/\+\-]+)(?:\s*\.)?$',
            r'(?<=answer:)\s*([0-9a-zA-Z\.\/\+\-]+)',
        ]
        for pattern in answer_patterns:
            matches = re.findall(pattern, response.lower())
            if matches:
                return matches[-1].strip()
        return None
    
    extracted_answers = []
    for start_pos in boxed_positions:
        brace_count = 1
        current_pos = start_pos
        while current_pos < len(response) and brace_count > 0:
            if response[current_pos] == '{':
                brace_count += 1
            elif response[current_pos] == '}':
                brace_count -= 1
            current_pos += 1
        
        if brace_count == 0:
            content = response[start_pos:current_pos-1]
            extracted_answers.append(content.strip())
    
    if not extracted_answers:
        return None

    # --- 增强的后处理逻辑 ---
    final_answer = extracted_answers[-1] # 取最后一个
    
    # 1. 去除首尾的引号、括号、空白
    final_answer = final_answer.strip().strip("'\"()")

    # 2. 处理 LaTeX 格式包裹 (如 \textbf{A}, \mathbf{B}, \text{C})
    # 循环去除，防止多重包裹 e.g. \textbf{\text{A}}
    while True:
        # 匹配 \command{content} 的形式
        latex_wrapper_match = re.match(r'^\\[a-zA-Z]+\{(.*)\}$', final_answer)
        if latex_wrapper_match:
            # 检查内部是否还有未闭合的括号，如果有则不拆（可能是公式 \frac{}{}）
            # 这里简单判断：如果去掉外层后，内部括号平衡，则认为是装饰性命令
            inner = latex_wrapper_match.group(1)
            # 简单的启发式：如果是选择题选项长度（很短），直接拆
            if len(inner) < 10: 
                final_answer = inner.strip()
            else:
                break # 长内容可能是公式，停止拆解
        else:
            break

    # 3. 再次去除可能暴露出来的括号
    final_answer = final_answer.strip().strip("'\"()")

    # 4. 专门针对选择题选项的提取 (A), (B), A, B
    # 匹配单个字母 A-E，可选的括号包围
    choice_match = re.match(r'^(\(?\s*[A-E]\s*\)?)$', final_answer, re.IGNORECASE)
    if choice_match:
        # 如果匹配到，只返回其中的字母，并转大写
        return re.sub(r'[^A-E]', '', final_answer, flags=re.IGNORECASE).upper()

    # 5. 处理 Yes/No/True/False
    bool_match = re.match(r'^(Yes|No|True|False)$', final_answer, re.IGNORECASE)
    if bool_match:
        return bool_match.group(1).capitalize()

    return final_answer

def process_jsonl_file(
    input_file,
    output_file,
    expected_field="answer",
    response_field="model_answer",
):
    """
    处理JSONL文件，提取答案并比较
    """
    processed_count = 0
    kept_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            processed_count += 1
            line = line.strip()
            if not line:
                continue
                
            try:
                data = json.loads(line)
                
                # 提取两个字段的答案
                output_answer = data.get(expected_field, "")
                model_answer = extract_boxed_answer_enhanced(data.get(response_field, ""))
                # 比较答案是否一致
                if output_answer and model_answer and output_answer.lower() == model_answer.lower():
                    # 删除output字段
                    data.pop(expected_field, None)
                    
                    # Replace the expected label with the model's full response.
                    if response_field in data:
                        data["answer"] = data.pop(response_field)
                    
                    # 写入输出文件
                    outfile.write(json.dumps(data, ensure_ascii=False) + '\n')
                    kept_count += 1
                else:
                    print(f"跳过第{processed_count}行: expected={output_answer}, model={model_answer}")
            except json.JSONDecodeError as e:
                print(f"第{processed_count}行JSON解析错误: {e}")
                continue
    
    ratio = kept_count / processed_count if processed_count else 0
    print(f"处理完成! 共处理{processed_count}行，保留{kept_count}行（{ratio:.2%}）")
    return {"processed": processed_count, "kept": kept_count, "ratio": ratio}
