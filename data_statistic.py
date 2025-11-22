import os
import json
from typing import List, Union, Dict, Any
from datetime import datetime

from transformers import AutoTokenizer

enc = AutoTokenizer.from_pretrained(
    "/home/zhwang/Model/Qwen3-8B-Base",
    trust_remote_code=True  # 如果模型使用了自定义 tokenizer
)

class DataStats:
    def __init__(self, target_field: str, tokenizer=None):
        self.target_field = target_field
        self.tokenizer = tokenizer if tokenizer else self.default_tokenizer
        self.result_per_file = {}  # 保存每个文件的统计数据
        self.global_token_sum = 0  # 全局 token 数总和

    def default_tokenizer(self, text: str) -> int:
        return len(enc.encode(text))

    # =====================================================================
    # 文件处理
    # =====================================================================
    def process_file(self, file_path: str):
        """统计单个文件并保存结果"""
        filename = os.path.basename(file_path)

        token_list = []
        count = 0

        if file_path.endswith(".json"):
            count, token_list = self._process_jsonl(file_path)
        elif file_path.endswith(".jsonl"):
            count, token_list = self._process_jsonl(file_path)
        else:
            return  # 忽略其他文件

        if count == 0:
            return

        token_sum = sum(token_list)
        self.global_token_sum += token_sum

        self.result_per_file[filename] = {
            "total_items": count,
            "token_avg": token_sum / count,
            "token_max": max(token_list),
            "token_min": min(token_list),
            "token_sum": token_sum,
        }

        # ===== 简洁终端输出 =====
        print(f"{filename} | count: {count} | avg_tokens: {token_sum / count:.2f}")

    def _process_json(self, file_path: str):
        token_list = []
        count = 0
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            for item in data:
                count, token_list = self._process_item(item, count, token_list)
        elif isinstance(data, dict):
            count, token_list = self._process_item(data, count, token_list)

        return count, token_list

    def _process_jsonl(self, file_path: str):
        token_list = []
        count = 0
        if not file_path:
            return []
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line)) 
        for item in data:
            count, token_list = self._process_item(item, count, token_list)  
        return count, token_list

    def _process_item(self, item, count, token_list):
        if self.target_field not in item:
            return count, token_list
        val = item[self.target_field]
        if not isinstance(val, str):
            return count, token_list
        token_list.append(self.tokenizer(val))
        return count + 1, token_list

    # =====================================================================
    # 输出到 log 文件
    # =====================================================================
    def save_log(self, log_dir="./statistic"):
        os.makedirs(log_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
        log_path = os.path.join(log_dir, f"{timestamp}.json")

        log_data = {
            "files": self.result_per_file,
            "global_token_sum": self.global_token_sum
        }

        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)

        print(f"\n详细统计已保存到: {log_path}")


# =====================================================================
# 收集文件
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
# 执行入口
# =====================================================================
if __name__ == "__main__":
    # 你只需修改这里即可
    input_paths = ["/home/zhwang/WKH/logic_tree_code/result/output/data_1116_1_train_story_success.json"]
    target_field = "DeepSeek-R1-answer"

    files = collect_files(input_paths)

    stats = DataStats(target_field)

    print("===== Processing Files =====")
    for f in files:
        stats.process_file(f)

    print(f"\nGlobal token sum: {stats.global_token_sum}")

    stats.save_log("./statistic")

