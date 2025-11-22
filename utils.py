import json

def save_jsonl(data, filename, mode = 'a'):
    if not isinstance(data, list):
        #raise ValueError("Data should be a list of dictionaries")
        data = [data]
    with open(filename, mode, encoding='utf-8') as f:
        for entry in data:
            json.dump(entry, f)
            f.write('\n')
def save_json(data, filename, mode='w'):
    with open(filename, mode, encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
def read_jsonl(filename=None):
    if not filename:
        return []
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))   
    return data
def print_tree(nested_list, indent=0):
    for item in nested_list:
        if isinstance(item, list):
            print_tree(item, indent + 4)
        else:
            print(" " * indent + str(item)+'\n')