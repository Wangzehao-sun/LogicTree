import os
import json
from typing import List, Union, Dict, Any
from datetime import datetime

from concurrent.futures import ProcessPoolExecutor, as_completed
from transformers import AutoTokenizer

def build_dict_from_jsonl(file_path):
    """
    读取jsonl文件，将每行数据的num字段作为key，step字段作为value，返回一个字典。

    :param file_path: jsonl文件路径
    :return: 字典 {num: step}
    """
    result_dict = {}
    step_dict = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                key = data.get('num')
                value = data.get('step')
                if value in step_dict.keys():
                    step_dict[value] += 1
                else:
                    step_dict[value] = 1
                if key is not None and value is not None:
                    result_dict[key] = value
            except json.JSONDecodeError:
                print(f"Warning: 无法解析这一行: {line}")
    
    print(f"文件{file_path}step比例统计：{step_dict}")
    
    return result_dict


# =====================================================================
# 全局加载 Tokenizer（每个进程各自加载一次）
# =====================================================================
# 顶层函数：chunk 处理函数
def chunk_worker(args):
    """
    处理单个 chunk 数据
    返回：
        count: 总条数
        token_list: token 数列表
        step_list: step 长度列表
        ratio_list: token/step 比例列表
        format_stats: 每个 format 的统计信息
    """
    chunk, target_field, tokenizer_path, step_dict = args

    from transformers import AutoTokenizer
    enc = AutoTokenizer.from_pretrained(tokenizer_path, trust_remote_code=True)

    def tokenize(x: str) -> int:
        return len(enc.encode(x))

    count = 0
    token_list = []
    step_list = []
    ratio_list = []
    format_stats = {}  # {fmt: {"count": x, "token_list": [], "step_list": [], "ratio_list": []}}

    for item in chunk:
        if target_field in item and isinstance(item[target_field], str):
            tks = tokenize(item[target_field])
            token_list.append(tks)
            count += 1

            # step 处理
            num = item.get("num")
            step_len = step_dict.get(num, 1)  # 避免除以0
            step_list.append(step_len)

            ratio = tks / step_len if step_len != 0 else 0
            ratio_list.append(ratio)

            # format 分类统计
            fmt = item.get("format", "UNKNOWN")
            if fmt not in format_stats:
                format_stats[fmt] = {"count": 0, "token_list": [], "step_list": [], "ratio_list": []}

            format_stats[fmt]["count"] += 1
            format_stats[fmt]["token_list"].append(tks)
            format_stats[fmt]["step_list"].append(step_len)
            format_stats[fmt]["ratio_list"].append(ratio)

    return count, token_list, step_list, ratio_list, format_stats



# =====================================================================
# 子进程执行的函数（并发单位）
# =====================================================================
def process_file_worker(args):
    """
    文件级 worker（单文件内部并行 chunk）
    返回：filename, 文件统计结果, token_sum
    """
    file_path, target_field, tokenizer_path, step_dict = args
    filename = os.path.basename(file_path)

    # 读取 jsonl 或 json 文件
    data = []
    if file_path.endswith(".jsonl") or file_path.endswith(".json"):
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                data.append(json.loads(line))
    # elif file_path.endswith(".json"):
    #     with open(file_path, "r", encoding="utf-8") as f:
    #         d = json.load(f)
    #         data = d if isinstance(d, list) else [d]

    if not data:
        return filename, None, 0

    # 切 chunk
    CHUNK_SIZE = 5000
    chunks = [data[i:i + CHUNK_SIZE] for i in range(0, len(data), CHUNK_SIZE)]

    from concurrent.futures import ProcessPoolExecutor

    total_count = 0
    total_tokens = []
    total_steps = []
    total_ratios = []
    total_format_stats = {}

    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(chunk_worker, (chunk, target_field, tokenizer_path, step_dict))
            for chunk in chunks
        ]
        for fut in futures:
            c, tks, steps, ratios, fmt_stats = fut.result()
            total_count += c
            total_tokens.extend(tks)
            total_steps.extend(steps)
            total_ratios.extend(ratios)

            # 合并 format 统计
            for fmt, info in fmt_stats.items():
                if fmt not in total_format_stats:
                    total_format_stats[fmt] = {"count": 0, "token_list": [], "step_list": [], "ratio_list": []}
                total_format_stats[fmt]["count"] += info["count"]
                total_format_stats[fmt]["token_list"].extend(info["token_list"])
                total_format_stats[fmt]["step_list"].extend(info["step_list"])
                total_format_stats[fmt]["ratio_list"].extend(info["ratio_list"])

    if total_count == 0:
        return filename, None, 0

    token_sum = sum(total_tokens)

    # 文件级统计
    result = {
        "total_items": total_count,
        "token_avg": token_sum / total_count,
        "token_max": max(total_tokens),
        "token_min": min(total_tokens),
        "token_sum": token_sum,
        "step_avg": sum(total_steps) / len(total_steps),
        "ratio_avg": sum(total_ratios) / len(total_ratios),
        "formats": {}
    }

    # format 统计
    for fmt, info in total_format_stats.items():
        lst_tokens = info["token_list"]
        lst_steps = info["step_list"]
        lst_ratios = info["ratio_list"]
        if not lst_tokens:
            continue
        result["formats"][fmt] = {
            "count": info["count"],
            "token_avg": sum(lst_tokens) / len(lst_tokens),
            "token_max": max(lst_tokens),
            "token_min": min(lst_tokens),
            "token_sum": sum(lst_tokens),
            "step_avg": sum(lst_steps) / len(lst_steps),
            "ratio_avg": sum(lst_ratios) / len(lst_ratios),
        }

    return filename, result, token_sum




# =====================================================================
# 主类（仅负责合并结果，不做具体统计）
# =====================================================================
class DataStats:
    def __init__(self, target_field: str):
        self.target_field = target_field
        self.result_per_file = {}
        self.global_token_sum = 0
        self.avgstep = 0
        self.num = 0
        self.avgtoken = 0

    def merge_result(self, filename, stat_dict, token_sum):
        """主进程合并统计结果"""
        if stat_dict is not None:
            self.result_per_file[filename] = stat_dict
            self.global_token_sum += token_sum

            # 终端简洁输出
            print(f"{filename} | count: {stat_dict['total_items']} | avg_tokens: {stat_dict['token_avg']:.2f}")

    def save_log(self, log_dir="./statistic"):
        """保存 log 文件"""
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
        log_path = os.path.join(log_dir, f"{timestamp}.json")

        log_data = {
            "files": self.result_per_file,
            "global_token_sum": self.global_token_sum,
        }

        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)

        print(f"\n详细统计已保存到: {log_path}")


# =====================================================================
# 文件收集
# =====================================================================
def collect_files(paths: Union[str, List[str]]) -> List[str]:
    if isinstance(paths, str):
        paths = [paths]

    res = []
    for p in paths:
        if os.path.isfile(p) and p.endswith((".json", ".jsonl")):
            res.append(p)
        elif os.path.isdir(p):
            for root, _, files in os.walk(p):
                for fname in files:
                    if fname.endswith((".json", ".jsonl")):
                        res.append(os.path.join(root, fname))
    return res


# =====================================================================
# 主程序（入口）
# =====================================================================
if __name__ == "__main__":
    tokenizer_path = "/home/zhwang/Model/Qwen3-8B-Base"
    input_paths = [
        "./result/output/data_1116_1_train_story_success.json",
        "./result/output/data_1116_1_train_choice_success.json"
    ]
    target_field = "DeepSeek-R1-answer"

    files = collect_files(input_paths)
    file_dict = {}
    file_dict["./result/output/data_1116_1_train_story_success.json"] = build_dict_from_jsonl("/home/zhwang/WKH/logic_tree_code/SymbolicLogicTree/rules_data_1116_1.jsonl")
    file_dict["./result/output/data_1116_1_train_choice_success.json"] = build_dict_from_jsonl("/home/zhwang/WKH/logic_tree_code/SymbolicLogicTree/rules_data_1116_1.jsonl")
    stats = DataStats(target_field)

    print(f"===== Processing Files (parallel={len(files)} tasks) =====")

    # 并发执行，每个文件一个 task
    with ProcessPoolExecutor(max_workers=4) as ex:
        futures = [
            ex.submit(process_file_worker, (file, target_field, tokenizer_path, file_dict[file]))
            for file in files
        ]

        for future in as_completed(futures):
            filename, result, token_sum = future.result()
            stats.merge_result(filename, result, token_sum)

    print(f"\nGlobal token sum: {stats.global_token_sum}")
    stats.save_log("./statistic")
