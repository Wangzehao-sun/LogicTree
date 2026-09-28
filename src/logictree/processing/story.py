"""Filter long-form responses when an expected boxed answer is available."""

from __future__ import annotations

import json

from .choice import extract_boxed_answer_enhanced
def process_jsonl_file(
    input_file,
    output_file,
    expected_field="output",
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
                output_answer = extract_boxed_answer_enhanced(data.get(expected_field, ""))
                model_answer = extract_boxed_answer_enhanced(data.get(response_field, ""))
                # 比较答案是否一致
                if output_answer and model_answer and output_answer.lower() == model_answer.lower():
                    # 删除output字段
                    data.pop(expected_field, None)
                    
                    # Replace the expected answer with the model's full response.
                    if response_field in data:
                        data["answer"] = data.pop(response_field)
                    
                    # 写入输出文件
                    outfile.write(json.dumps(data, ensure_ascii=False) + '\n')
                    kept_count += 1
                    print(f"保留第{processed_count}行: {model_answer}")
                # else:
                    # print(f"跳过第{processed_count}行: output={output_answer}, DeepSeek={deepseek_answer}")
                    
            except json.JSONDecodeError as e:
                print(f"第{processed_count}行JSON解析错误: {e}")
                continue
    
    ratio = kept_count / processed_count if processed_count else 0
    print(f"处理完成! 共处理{processed_count}行，保留{kept_count}行")
    return {"processed": processed_count, "kept": kept_count, "ratio": ratio}
