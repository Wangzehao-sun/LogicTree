from re import sub
import sys,json
from utils import read_jsonl, save_jsonl, save_json
import logging,random

output0 = {
  "example1": {
    "propositions": {
      "Q0":"The spread of the disease was effectively contained.", 
      "P0": "The government initiated a nationwide vaccination campaign.",
      "R0(x)": "Region x has achieved full vaccination coverage.",
      "T0": "Vaccination rates across regions increased significantly.",
      #"a": "Region Z"
    },
    "rules": [
      {
        "rule1": "∀x (~R0(x)).",
        "explanation": "No region has achieved full vaccination coverage."
      },
      {
        "rule2": "(P0 → T0).",
        "explanation": "If the government initiated a nationwide vaccination campaign, then vaccination rates across regions increased significantly."
      },
      {
        "rule3": "(T0 → Q0).",
        "explanation": "If vaccination rates increased significantly, then the spread of the disease was effectively contained."
      },
      {
        "rule4": "(P0 | R0(a)).",
        "explanation": "Either the government initiated a nationwide vaccination campaign, or region Z has achieved full vaccination coverage."
      },
    ],
    "options": [
      {
        "option1": "Q0",
        "explanation": "The spread of the disease was effectively contained."
      },
      {
        "option2": "~R0(a)",
        "explanation": "Region Z has not achieved full vaccination coverage."
      },
    ]
  }

}
example0 = (
    "####Logic Rules:['rule1: ∀x (~R0(x)).', 'rule2: (P0 → T0).', 'rule3: (T0 → Q0).', 'rule4: (P0 | R0(a)).']\n"
    "####Logic Options:['option1: Q0.', 'option1: ~R0(a).']\n"
    f"##Output: {output0}\n"
    "------------\n"
)
output1= {
  "example1": {
    "propositions": {
      "P0": "The system's primary server is operational.",
      "P1": "The backup server has been activated.",
      "P2": "Critical data has been successfully backed up.",
      "P3": "A minor software update has been applied.",
      "S0": "The firewall configuration is incorrect.",
    },
    "rules": [
      {
        "rule1": "(P1 > (~((~P0) & Q))).",
        "explanation": "If the backup server has been activated, then it must be the case that the statement 'the primary server is not operational and critical data has been successfully backed up' is not true. "
      },
      {
        "rule2": "((~P2) | P1).",
        "explanation": "Either critical data has not been successfully backed up, or the backup server has been activated,or both."
      },
      {
        "rule3": "((~P3) > S0).",
        "explanation": "If a minor software update has not been applied, then the firewall configuration is incorrect."
      },
    ],
    "options": [
      {
        "option1": "P3",
        "explanation": "A minor software update has been applied."
      },
      {
        "option2": "~P2",
        "explanation": "Critical data has not been successfully backed up."
      },
    ]
  }
}
example1 = (
    "####Logic Rules:['rule1: (P1>(~((~P0)&(Q)))).', 'rule2: ((~P2)|P1).', 'rule3: ((~P3)>S0).']\n"
    "####Logic Options:['option1: P3.', 'option2: ~P2.']\n"
    f"##Output: {output1}\n"
    "------------\n"
)
output2 = {
    "example1": {
        "propositions": {
            "P0": "The camera's shutter speed is set to capture fast-moving subjects.",
            "P1": "The camera's aperture is adjusted for optimal depth of field.",
            "P2": "The photograph is taken during golden hour.",
            "P3": "The photographer uses a tripod for stability.",
            "P4": "The camera's ISO setting is adjusted for low light conditions.",
            "P5": "The lens is clean and free of smudges.",
            "P6": "The photograph is in focus.",
            "Q0": "The photograph is intended for a professional portfolio."
        },
        "rules": [
            {
                "rule1": "((P1 & P2) > ((~Q0) > P0)).",
                "explanation": "If the camera's aperture is adjusted for optimal depth of field and the photograph is taken during golden hour, then if the photograph is not intended for a professional portfolio, the shutter speed must be set to capture fast-moving subjects."
            },
            {
                "rule2": "(P4 > P1).",
                "explanation": "If the camera's ISO setting is adjusted for low light conditions, then the camera's aperture is adjusted for optimal depth of field."
            },
            {
                "rule3": "P4.",
                "explanation": "The camera's ISO setting is adjusted for low light conditions."
            },
            {
                "rule4": "(P3 | P2).",
                "explanation": "Either the photographer uses a tripod for stability, or the photograph is taken during golden hour, or both."
            },
            {
                "rule5": "((P5 & P6) > (~P3)).",
                "explanation": "If the lens is clean and free of smudges and the photograph is in focus, then the photographer does not use a tripod for stability."
            },
            {
                "rule6": "P5.",
                "explanation": "The lens is clean and free of smudges."
            },
            {
                "rule7": "P6.",
                "explanation": "The photograph is in focus."
            },
            {
                "rule8": "(~P0).",
                "explanation": "The camera's shutter speed is not set to capture fast-moving subjects."
            }
        ],
        "options": [
            {
                "option1": "P2.",
                "explanation": "The photograph is taken during golden hour."
            },
            {
                "option2": "P3.",
                "explanation": "The photographer uses a tripod for stability."
            },
            {
                "option3": "~((~Q0) > P0).",
                "explanation": "It is not the case that if the photograph is not intended for a professional portfolio, the shutter speed must be set to capture fast-moving subjects."
            },
            {
                "option4": "~Q0.",
                "explanation": "The photograph is not intended for a professional portfolio."
            }
        ],
        "conclusion": {
            "conclusion": "Q0.",
            "explanation": "The photograph is intended for a professional portfolio."
        },
    },
}
example2 = (
    "####Logic Rules:['rule1: ((P1&P2)>((~Q0)>P0)).', 'rule2: (P4>P1).', 'rule3: P4.', 'rule4: (P3|P2).', 'rule5: ((P5&P6)>(~P3)).', 'rule6: P5.', 'rule7: P6.', 'rule8: (~P0).']\n"
    "####Logic Options:['option1: P2.', 'option2: P3.', 'option3: ~((~Q0)>P0).', 'option4: ~Q0.']\n"
    "####Conclusion: Q0"
    f"##Output: {output2}\n"
    "------------\n"
)
def choose_domain(domain_list, num):
    return ", ".join(random.sample(domain_list, num))

def generate_rules_prompt(rules,options,domain,conclusion):
    prompt = (
        "You are a highly skilled logic analyst with expertise in understanding and interpreting complex logical relationships."
        #"You have a deep understanding of logical symbols and their meanings, and you excel at translating abstract concepts into complex events while maintaining the integrity of logical rules.\n"
        "##Instruction:\n1.Please thoroughly and deeply understand the logical rules between the propositions provided below.Note the meanings of the logical symbols:\n"
        "   - '~' (NOT): Negation, indicates the proposition is not true.\n"
        "   - '→' (IMPLIES):Implies, indicates that there is a causal or inferential relationship between the two propositions.\n"
        "   - '|' (OR): Logical disjunction, indicates that at least one of the propositions on either side is true.\n"
        "   - '&' (AND): Logical conjunction, indicates that both propositions on either side are true.\n"
        "   - '∀x' (FOR ALL): Universal quantifier, indicates that a statement is true for all values of x.\n"
        #"   - '⊕' (XOR): Exclusive OR, indicates that  two propositions cannot both be true simultaneously.\n"
        #"   - \n"
        "2. Following the given logical rules, replace each symbolic proposition (e.g., P, Q, R) with a specific, real-life event. The key requirements are as follows: "
        "    * Thematic Coherence: All events must originate from a single, coherent domain or scenario (e.g., a criminal investigation, a software development project, a medical diagnosis process, etc.). "
        "    * Plausible Logic: The relationships between the events must not only satisfy the abstract logical rules but also possess strong real-world plausibility, causality, or inherent connection, making the combination sound natural and aligned with common sense."
        #"3. For each rule, Use the above events to generate a short story that rule."
        "3. Use the corresponding events to explain each logic rule expression in natural language. Do not include the entity labels like P, Q, R, S, T in the context.Please do not add, modify, or delete any rule.\n"
        #"4. Use the corresponding events to explain each logic option expression in natural language. Do not include the entity labels like P, Q, R, S, T in the context.\n"
        "4. Please follow the priority order in the logical expression, think step by step, and ensure the translation is accurate and clear. "
        "You can refer to the examples of translation below and enhance the language diversity while ensuring the semantics remain unchanged. For example:\n"
        "  i: P1→(~((~P0)&Q))----If P1 is true, then it must be the case that the statement 'both P0 is false and Q is true' is not true.\n"
        "  ii: (~(Q|R0))→P2----If both Q and R0 are false, then P2 must be true.\n"
        "  iii:(~P2)|(P0|Q)----Either P2 is false, or at least one of P0 or Q is true.\n"
        "  iv: ((P1&P2)→((~Q)>P0))----If both P1 and P2 are true, then [if Q is false, P0 must also be true.].\n"
        "  v: (∀x(P4(x)))----For all x, P4(x) is true.\n"
        #"6. Generte 1 examples from multiple domains."
        #"4. Finally, Use the corresponding events to explain the following complex reasoning question.\n"
        f"6. Please select a field from the [{domain}] that most easily satisfies the above logical relationships, and generate 1 example. We hope you can leverage relevant entities in this field to construct the aforementioned complex events.\n"
        "Please strictly follow the JSON format below, and ensure that every rule and option is fully translated. Output the propositions and their corresponding events in the json format:{\"example1\":{\"propositions\":{\"Q0\":***,...},\"rules\":[{\"rule1\":***,\"explaination\":***,},...],\"options\":[{\"option1\":***,\"explaination\":***,},...],\"conclusion\":{\"conclusion\":***,\"explanation\":***}},...}.\n"
        f"----example1----\n{example2}"
        f"####Logic Rules:{rules}\n"
        f"####Logic Options:{options}\n"
        f"####Conclusion:{conclusion}\n"
        "##Output:"
        #f"##Question:{question}"
    )
    return prompt

def merge_all_domains_to_list(file_path):
    all_items = []
    try:
        with open(file_path,'r',encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
          # 处理列表类型
          for version in data:
              for sub_categories in version.values():
                  for item_list in sub_categories.values():
                      all_items.extend(item_list)
      
        elif isinstance(data, dict):
            # 处理字典类型
          for sub_categories in data.values():
              for item_list in sub_categories.values():
                    all_items.extend(item_list)

        
    except FileNotFoundError:
        print(f"错误：文件未找到 at {file_path}")
    except json.JSONDecodeError:
        print(f"错误：无法解析JSON文件 at {file_path}")
    except Exception as e:
        print(f"发生未知错误：{e}")
    
    return all_items

def generate_data_with_llm_v1_prompts(data_list,domain_list,pt=False):
    results = []
    for data in data_list:
        logic_rules = data['rules']
        conclusion = data['conclusion']
        options = []
        j = 1
        for key,value in data['options'].items():
            options.extend([f"option{i+j}: {v}." for i,v in enumerate(value)])
            j+=len(value)
        for i in range(10):
            newdata = data.copy()
            domain = choose_domain(domain_list,num=5)
            prompt = generate_rules_prompt(logic_rules,options,domain,conclusion)
            newdata['prompt'] = prompt
            newdata['domain'] = domain
            results.append(newdata)
    print(len(results))
    return results


if __name__ == '__main__':
    filename = sys.argv[1]
    save_file = sys.argv[2]
    logging.getLogger().setLevel(logging.ERROR)
    data_list = read_jsonl(filename)
    domain_list = merge_all_domains_to_list("domain.json")
    results = []
    results = generate_data_with_llm_v1_prompts(data_list,domain_list)
    save_jsonl(results,save_file, mode='w')