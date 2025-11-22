import sys,json
from utils import read_jsonl, save_jsonl

def process_generated_data_v1(data):
    res = []
    for item in data:
        # print(item["num"])
        leaf_nodes = item["leaf_nodes"]
        example_keys = ["example1"]
        reasoning_steps = item["reasoning_steps"]
        for example in example_keys:
            if example not in item.keys():
                print(f"Error: {example} not in item")
                print(item["num"])
                continue
            if item[example] == "":
                continue
            flag = False
            possible_keys = ["propositions","rules","options"]
            for key in possible_keys:
                if key not in item[example].keys():
                    print(f"Error: {key} not in {example}")
                    print(item["num"])
                    flag = True
                    break
            if flag:
                continue
            e_propositions = item[example]["propositions"]
            #print(e_propositions)
            e_rules = item[example]["rules"]
            
            for leaf,rule in zip(leaf_nodes,e_rules):
                try:
                    rule_key = list(rule.keys())[0]
                    rule_exp = rule[rule_key].replace(" ","").replace(".","")
                except:
                    flag = True
                    break
                if leaf != rule_exp and leaf[1:-1]!= rule_exp:
                    print(f"Error: leaf {leaf} not equal rule {rule_exp}")
                    print(item["num"])
                    #flag = True
            if flag:
                continue
            if len(e_rules) != len(item["leaf_nodes"]):
                print(f"Error: rules {len(e_rules)} not equal to leaf nodes {len(item['leaf_nodes'])}")
                print(item["num"])
                continue
            e_options = item[example]["options"]
            #print(len(e_options))
            try:
                conclusions = [
                    {"conclusion":e_options[0]["explanation"],"answer":"Yes"},
                #{"conclusion2":e_options[1]["explanation"],"answer":"No"},
                #{"conclusion3":e_options[2]["explanation"],"answer":"Uncertain"}
                ]
                for i,o in enumerate(e_options[1:]):
                    conclusions.append({f"conclusion":o["explanation"],"answer":"No"})
            except Exception as e:
                print(f"Error processing options: {e}")
                print(item["num"])
                continue
            try:
                context = [f"rule{i+1}. {r['explanation']}" for i,r in enumerate(e_rules)]
            except Exception as e:
                print(f"Error processing context: {e}")
                print(item["num"])
                continue
            res.append({
                "num":item["num"],
                "step":item["step"],
                "logic_tree":item["logic_tree"],
                "leaf_nodes":item["leaf_nodes"],
                "entities":e_propositions,
                "rules":e_rules,
                "reasoning_steps":reasoning_steps,
                "options":e_options,
                # "conclusions":conclusions,
            })
    return res


if "__main__" == __name__:
    filename = sys.argv[1]
    save_file = sys.argv[2]
    data_list = read_jsonl(filename)
    result = []
    for line in data_list:
        temp = line["DeepSeek-R1-answer"]
        index_start = temp.find('{')
        index_end = temp.rfind('}')
        res =None
        target = temp
        if index_start !=-1:
            target = temp[index_start:index_end+1]
        try:
            res = json.loads(target)
        except:
            res = {"error":"json parse error"}
            continue
        new_line = line.copy()
        new_line.update(res)
        del new_line["DeepSeek-R1-answer"]
        result.append(new_line)
    new_result = process_generated_data_v1(result)
    save_jsonl(new_result, save_file, 'w')