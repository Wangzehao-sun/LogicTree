import random, re
import json
from logictree.io import read_jsonl, save_jsonl

def clean_result(text):
    # 去掉连续的两个~符号
    cleaned_line = re.sub(r'~\(~\((.+)\)\)',r'\1',text) #
    cleaned_line = re.sub(r'\(~\(~([^\(\)&|~>⊕]+)\)\)',r'\1',cleaned_line) #
    cleaned_line = re.sub(r'~\(~([^\(\)&|~>⊕]+)\)',r'\1',cleaned_line)
    return cleaned_line

def clean_result_list(text_list):
    cleaned_list = []
    for text in text_list:
        cleaned_list.append(clean_result(text))
    return cleaned_list

def process_data(data):
    processed_data = []
    for item in data:
        rules = []
        for i,rule in enumerate(item["leaf_nodes"]):
            rules.append(f"rule{i+1}: {rule}.")
        reasoning_steps = []
        for i,step in enumerate(item["reasoning_process"]):
            premises = ", ".join(step["Premises"])
            conclusion = step["Conclusion"]
            reasoning_steps.append(f"step{i+1}: Given that [{premises}], it can be deduced that [{conclusion}].\n")
        #choice_question = random.choice(choice_template)
        #smallest_values = heapq.nsmallest(3, item["inodes"], key=len)
        option1_4 = item["inodes"][-4:]
        random.shuffle(option1_4)
        correct_option = [option1_4[0]]
        contradictory_option = [clean_result("~"+o) for o in option1_4[1:]]
        #unrelated_option = random.choice(["U","V","U>V","U|V","~U"])
        options = {
            "correct": correct_option,
            "uncorrect": contradictory_option,
        }
        processed_data.append({
            "num": item["num"],
            "step": item["step"],
            "logic_tree": item["logic_tree"],
            "leaf_nodes": item["leaf_nodes"],
            "inodes": item["inodes"],
            "rules": rules,
            "reasoning_steps": reasoning_steps,
            "options": options,
            "conclusion":item["logic_tree"][0]
        })
    return processed_data

data = read_jsonl("data/symbolic/rules_data_1116_1.jsonl")
processed_data = process_data(data)
save_jsonl(processed_data, "outputs/prepared/data_1116_1.jsonl")
