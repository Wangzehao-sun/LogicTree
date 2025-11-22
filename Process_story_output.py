import json
import sys
def process_jsonl_file(input_file, output_file):
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
                output_answer = extract_boxed_answer_enhanced(data.get("output", ""))
                deepseek_answer = extract_boxed_answer_enhanced(data.get("DeepSeek-R1-answer", ""))
                # 比较答案是否一致
                if output_answer and deepseek_answer and output_answer.lower() == deepseek_answer.lower():
                    # 删除output字段
                    if "output" in data:
                        del data["output"]
                    
                    # 重命名DeepSeek-R1-answer为answer
                    if "DeepSeek-R1-answer" in data:
                        data["answer"] = data.pop("DeepSeek-R1-answer")
                    
                    # 写入输出文件
                    outfile.write(json.dumps(data, ensure_ascii=False) + '\n')
                    kept_count += 1
                    print(f"保留第{processed_count}行: {deepseek_answer}")
                # else:
                    # print(f"跳过第{processed_count}行: output={output_answer}, DeepSeek={deepseek_answer}")
                    
            except json.JSONDecodeError as e:
                print(f"第{processed_count}行JSON解析错误: {e}")
                continue
    
    print(f"处理完成! 共处理{processed_count}行，保留{kept_count}行")

if __name__ == "__main__":
    # 设置文件路径
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # 处理文件
    process_jsonl_file(input_file, output_file)
