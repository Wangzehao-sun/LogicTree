import random,sys
from utils import save_jsonl, read_jsonl
choice_template = [
    "From the above premises, which of the following options can be deduced as a conclusion?",
    "Based on the given premises, which of the following options can logically be concluded?",
    "According to the above premises, which option can be inferred as a conclusion?",
    "Given the premises above, which of the following options can be concluded?",
    "Using the provided premises, which option can be derived as a conclusion?",
    "Which of the following options can be drawn as a conclusion based on the above premises?",
]
example = (
'''
1. Analysis of Problem Goal and Understanding Premise Meanings

The objective of this analysis is to determine the specific medical status of the patient by synthesizing 11 provided premises. These premises contain both factual observations (such as MRI results and symptoms) and logical rules (diagnostic criteria). We need to deduce hidden facts—specifically regarding autoantibodies, blood test results, and pancreatic function—to verify which of the proposed conclusions is logically valid.

Key aspects to understand:
- The diagnosis of "Pancreatic Dysfunction" is a composite state requiring both structural issues (from imaging) and functional issues (from blood tests).
- There is a strict logical chain concerning the "Rare Endocrine Disorder": it is a potential diagnosis that only triggers if the patient has autoantibodies but fails to show insulin secretion abnormalities.
- The "Family History" and "Autoantibodies" premises form an "Either/Or" structure, allowing us to use elimination to find the truth.

2. Step-by-Step Reasoning

Step 1: Determining the results of the imaging (MRI)
* Premise Basis: Premise 4 (High-resolution MRI performed), Premise 5 (Radiological findings indicate pancreatic atrophy), Premise 3 (Rule regarding structural abnormalities).
* Reasoning: Premise 4 and Premise 5 confirm that the specific conditions for the rule in Premise 3 are met. The rule states that if an MRI is performed and atrophy is found, then imaging shows structural abnormalities. Since the procedure was done and the specific finding was present, the conclusion is inevitable.
* Conclusion: Imaging shows structural abnormalities in the pancreas.

Step 2: Determining the patient's autoantibody status
* Premise Basis: Premise 9 (Patient does not require immediate insulin), Premise 6 (Rule regarding family history), Premise 8 (Rule: Family History OR Autoantibodies).
* Reasoning: First, we look at Premise 6, which says, "If the patient has a family history, they require immediate insulin." However, Premise 9 states the patient does NOT require immediate insulin. By reasoning backwards (denying the consequence), we conclude the patient does not have a family history. Next, we look at Premise 8, which states the patient must have either a family history OR tests positive for autoantibodies (or both). Since we have ruled out the family history, the patient must test positive for autoantibodies.
* Conclusion: The patient tests positive for autoantibodies associated with type 1 diabetes.

Step 3: Determining the results of the blood tests
* Premise Basis: Step 2 Conclusion (Antibodies positive), Premise 7 (Conditional rule regarding rare disorders), Premise 10 (Patient is not diagnosed with a rare disorder).
* Reasoning: Since we established in Step 2 that the patient is antibody-positive, the conditional rule in Premise 7 becomes active. The rule effectively says: "In this patient, if blood tests do NOT confirm abnormal insulin secretion, then they are diagnosed with a rare endocrine disorder." However, Premise 10 tells us the patient is NOT diagnosed with a rare endocrine disorder. Therefore, the condition that leads to the rare disorder must be false. The condition was "blood tests do not confirm abnormal secretion." Since this is false, the opposite is true.
* Conclusion: Blood tests confirm abnormal insulin secretion.

Step 4: Confirming the final diagnosis of pancreatic dysfunction
* Premise Basis: Step 1 Conclusion (Structural abnormalities present), Step 3 Conclusion (Abnormal secretion confirmed), Premise 2 (Rule for confirming dysfunction).
* Reasoning: Premise 2 states that if imaging shows structural abnormalities AND blood tests confirm abnormal secretion, then the endocrinologist confirms pancreatic dysfunction. We have proven both required conditions in Step 1 and Step 3. Consequently, the diagnosis is confirmed.
* Conclusion: The endocrinologist confirms pancreatic dysfunction.

3. Analysis of Options Based on Reasoning

Option (A): If blood tests do not confirm abnormal insulin secretion, then the patient is diagnosed with a rare endocrine disorder.
* Analysis: This option restates the logical rule from Premise 7. Since we proved in Step 2 that the patient is positive for autoantibodies, this specific conditional relationship is valid for this patient. Even though the blood tests actually *did* confirm the abnormality, the logical statement "If they hadn't, the patient would be diagnosed with the rare disorder" remains true.
* Verdict: Correct.

Option (B): It is not the case that elevated blood glucose levels imply a diagnosis of diabetes mellitus.
* Analysis: In Step 4, we confirmed Pancreatic Dysfunction. Combined with Premise 11 (Patient has symptoms), all conditions for Premise 1 are met. Premise 1 states that under these conditions, elevated glucose implies diabetes. Option B claims this implication is false, which contradicts the established logic.
* Verdict: Incorrect.

Option (C): The endocrinologist does not confirm pancreatic dysfunction.
* Analysis: This contradicts the specific conclusion of Step 4, where we proved that all criteria for dysfunction were met.
* Verdict: Incorrect.

Option (D): Blood tests do not confirm abnormal insulin secretion.
* Analysis: This contradicts the specific conclusion of Step 3. We proved via logical negation that the blood tests must have confirmed the abnormality, otherwise the patient would have been diagnosed with the rare disorder.
* Verdict: Incorrect.

4. Final Answer
Therefore, the only logically valid conclusion based on the premises and reasoning is \\boxed{(A)}.

'''
)
# def generate_question(data):
#     res = []
#     num = 0
#     for d in data:
#         num+=1
#         item = d
#         context = [f'{i+1}. {s['explanation']}' for i, s in enumerate(item['rules'])]
#         context = "".join
#         conclusions = []
#         for i,o in enumerate(item['options']):
#             conclusions.append(
#                 {
#                     "conclusion": o['conclusion'],
#                     "num":i
#                 }
#             )
#         res.append(
#             {
#                 "num":d['num'],
#                 "context":context,
#                 "conclusions":conclusions,
#             }
#         )
#     return res


# def generate_choice_train_data(data,is_rational):
#     res = []
#     for item in data:
#         context = item['context']
#         question = random.choice(choice_template)
#         options_list = []
#         correct_option_index = None
        
#         # 打乱 conclusions 顺序
#         conclusions = item['conclusions'].copy()
#         random.shuffle(conclusions)
        
#         # 组装选项并确定正确答案
#         for i, c in enumerate(conclusions):
#             option_text = c['conclusion']
#             options_list.append(f"({chr(65+i)}) {option_text}")
#             if c['num'] == 0:
#                 correct_option_index = i
#         answer = chr(65 + correct_option_index)
#         options = "\n".join(options_list)
#         tmp = {
#                 "num":item['num'],
#                 "instruction" : f"Please use the context that contains relevant information, answer the following logical reasoning question. "
#                 "Please reason step by step, and put your final answer within \\boxed{}.\n\n"
#                 f"##Context:{context}"
#                 f"##Question: {question}\n{options}\n",
#                 "output":f"##Answer: The correct option is \\boxed{({answer})}.",

#                 } 
#         res.append(tmp)
#     return res

import random

def generate_question(data):
    res = []
    num = 0
    for d in data:
        try:
            # 检查必需的键是否存在
            if 'rules' not in d or 'options' not in d or 'num' not in d:
                print(f"跳过数据项 {num}: 缺少必需的键")
                continue
                
            item = d
            # 安全地构建context
            context_parts = []
            if 'rules' in item and isinstance(item['rules'], list):
                for i, s in enumerate(item['rules']):
                    if isinstance(s, dict) and 'explanation' in s:
                        context_parts.append(f'{i+1}. {s["explanation"]}')
                    else:
                        print(f"跳过数据项 {num}: 规则 {i} 格式不正确")
                        continue
            else:
                print(f"跳过数据项 {num}: rules 格式不正确")
                continue
                
            context = "".join(context_parts)
            
            # 安全地构建conclusions
            conclusions = []
            try:
                e_options = item['options']
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
            # if 'options' in item and isinstance(item['options'], list):
            #     for i, o in enumerate(item['options']):
            #         if isinstance(o, dict) and 'explanation' in o:
            #             conclusions.append({
            #                 "conclusion": o['explanation'],
            #                 "num": i
            #             })
            #         else:
            #             print(f"跳过数据项 {num}: 选项 {i} 格式不正确")
            #             continue
            # if 'conclusions' in item and isinstance(item['conclusions'], list):
            #     for i, c in enumerate(item['conclusions']):
            #         if isinstance(c, dict) and 'conclusion' in c:
            #             conclusions.append({
            #                 "conclusion": c['conclusion'],
            #                 "answer": c['answer'],
            #                 "num": i
            #             })
            #         else:
            #             print(f"跳过数据项 {num}: 结论 {i} 格式不正确")
            #             continue
            # else:
            #     print(f"跳过数据项 {num}: conclusions 格式不正确")
            #     continue
                
            res.append({
                "num": item['num'],
                "entities":item['entities'],
                "reasoning_steps":item['reasoning_steps'], 
                "context": context,
                "conclusions": conclusions,
            })
            num += 1
            
        except KeyError as e:
            print(f"跳过数据项 {num}: KeyError - {e}")
            continue
        except Exception as e:
            print(f"跳过数据项 {num}: 其他错误 - {e}")
            continue
            
    return res

def generate_choice_train_data(data, is_rational):
    res = []
    
    for item_idx, item in enumerate(data):
        try:
            # 检查必需的键是否存在
            if 'context' not in item or 'conclusions' not in item or 'num' not in item:
                print(f"跳过训练数据项 {item_idx}: 缺少必需的键")
                continue
                
            context = item['context']
            reasoning = item['reasoning_steps']
            entities = item['entities']
            
            # 安全地获取问题模板
            if not choice_template:
                print(f"跳过训练数据项 {item_idx}: choice_template 为空")
                continue
                
            question = random.choice(choice_template)
            options_list = []
            correct_option_index = None
            
            # 安全地处理conclusions
            if not isinstance(item['conclusions'], list) or len(item['conclusions']) == 0:
                print(f"跳过训练数据项 {item_idx}: conclusions 格式不正确或为空")
                continue
                
            # 打乱 conclusions 顺序
            conclusions = item['conclusions'].copy()
            random.shuffle(conclusions)
            
            # 组装选项并确定正确答案
            for i, c in enumerate(conclusions):
                if not isinstance(c, dict) or 'conclusion' not in c:
                    print(f"跳过训练数据项 {item_idx}: 结论 {i} 格式不正确")
                    continue
                    
                option_text = f"({chr(65+i)}) {c['conclusion']}"
                options_list.append({
                    "option": option_text,
                    "truth": c['answer']
                })
                if c['answer'] == "Yes":
                    correct_option_index = i
            
            # 检查是否找到了正确答案
            if correct_option_index is None:
                print(f"跳过训练数据项 {item_idx}: 未找到正确答案 (num=0)")
                continue
                
            if not options_list:
                print(f"跳过训练数据项 {item_idx}: 选项列表为空")
                continue
                
            answer = chr(65 + correct_option_index)
            options = options_list
            options_text = "\n".join([opt['option'] for opt in options_list])
            # tmp = {
            #     "num": item['num'],
            #     "instruction": f"Please use the context that contains relevant information, answer the following logical reasoning question. "
            #     "Please understand the providing reasoning steps, translate it into natual language, and put your final answer within \\boxed{}.\n\n"
            #     f"##Context:{context}"
            #     f"##Question: {question}\n{options}\n"
            #     f"##Reasoning Steps:{reasoning}\n",
            #     "output": f"##Answer: The correct option is \\boxed{({answer})}.",
            # } 
            prompt = {
                "num": item['num'],
                "context": context,
                "options": options,
                "answer": answer,
                # "instruction":"##Instruction:1. The following is a logical reasoning question and some conclusions. For each conclusion,the truth value can be Yes or No. And We have extracted the main event entities and logic expressions from the context and conclusions.\n"
                # "Note the meanings of the logical symbols:\n"
                # "   - '~' (NOT): Negation, indicates the proposition is not true.\n"
                # "   - '→' (IMPLIES):Implies, indicates that there is a causal or inferential relationship between the two propositions.\n"
                # "   - '|' (OR): Logical disjunction, indicates that at least one of the propositions on either side is true.\n"
                # "   - '&' (AND): Logical conjunction, indicates that both propositions on either side are true.\n"
                # "   - '∀x' (FOR ALL): Universal quantifier, indicates that a statement is true for all values of x.\n"
                # "2. Please refer to the following symbolic reasoning steps and the extracted entities to provide a detailed reasoning explanation in natural language."
                # "For each step, explain in natural language which specific premise or previous inference result is utilized as input, then translate this into its corresponding formal logical expression. Subsequently, declare the exact logical rule applied for the deduction, and finally state the derived conclusion in natural language."
                # #"For each step of reasoning, we provide the given premises and the conclusions that can be deduced. Please explain each step in detail.\n"
                # "3. Then, for each conclusion, refer to the reasoning process generated above and provide an explanation that aligns with the corresponding answer.\n"
                # "4. Finally, output the detailed reasoning process and the correct option. Please put your final answer within \\boxed{}.\n"
                # # f"----example1----\n{example2}"
                # f"####Context:{context}\n"
                # f"####Conclusions: {options}\n" 
                # f"####Entities:{entities}\n"  
                # f"####Reasoning Steps:{reasoning}\n"
                # "##Output:",
                "instruction": generate_reasoning_prompt(entities,options_text,context,reasoning),
                #"output": f"##Answer: The correct option is \\boxed{({answer})}.",
            }
            
            # res.append(tmp)
            res.append(prompt)
            
        except KeyError as e:
            print(f"跳过训练数据项 {item_idx}: KeyError - {e}")
            continue
        except IndexError as e:
            print(f"跳过训练数据项 {item_idx}: IndexError - {e}")
            continue
        except Exception as e:
            print(f"跳过训练数据项 {item_idx}: 其他错误 - {e}")
            continue
            
    return res 

def generate_reasoning_prompt(entities,options,context,reasoning):
    prompt = (
f'''
Your task is to generate a rigorous, detailed, and coherent natural language reasoning process. You will be provided with a logical problem (Context and Options) and a Symbolic Reasoning Reference (including Entity-to-Symbol mapping and a Symbolic Deduction path).
Your goal is to interpret the underlying logic of the provided Symbolic Chain and articulate the reasoning process entirely in natural, narrative English. Use the symbolic steps as a logical blueprint to ensure accuracy, but do not simply translate the symbols.

### Input Data Description
1.  **Context**: The natural language premises of the problem.
2.  **Entity Mapping**: The correspondence between natural language phrases and logical symbols (e.g., P: "Patient has fever").
3.  **Symbolic Chain**: The step-by-step logical derivation in symbolic form (e.g., Step 1: P & Q -> R).
4.  **Options**: The conclusions to verify.

### Output Structure Requirements
You must format your response exactly as follows:

**1. Analysis of Problem Goal and Premise Meanings**
Briefly summarize the goal and explain the key logical relationships defined in the premises (e.g., conditional rules, exclusions) based on the Context.

**2. Step-by-Step Reasoning**
Interpret the logical flow presented in the "Symbolic Chain" and construct a detailed natural language deduction for each step.
* **Step [N]: [Brief Title of the Step]**
    * *Premises:* [List the Premise numbers or previous Step results used.]
    * *Reasoning:* [Articulate the logic in clear English. Describe how the facts and rules interact to reach the conclusion. Ensure the narrative is fluent and strictly follows the logic of the symbolic reference.]
    * *Conclusion:* [State the factual conclusion of this step clearly.]

**3. Analysis of Options**
Evaluate each option based on the facts derived in the Step-by-Step Reasoning. Explicitly state why an option is "Correct" or "Incorrect" by referencing your deduced conclusions.

**4. Final Answer**
Conclude by clearly stating the correct option within \\boxed{{}}.

---
### Example (Reference)
Please refer to the following example for the expected output format and style:
{example}
---
### Input
**Context**:
{context}

**Entity Mapping**:
{entities}

**Symbolic Chain**:
{reasoning}

**Options**:
{options}
### Output：
'''

        # "##Instruction:1. The following is a logical reasoning context and some conclusions. For each conclusion,the truth value can be Yes, No or Uncertain. And We have extracted the main event entities and logic expressions from the context and conclusions.\n"
        # "Note the meanings of the logical symbols:\n"
        # "   - '~' (NOT): Negation, indicates the proposition is not true.\n"
        # "   - '→' (IMPLIES):Implies, indicates that there is a causal or inferential relationship between the two propositions.\n"
        # "   - '|' (OR): Logical disjunction, indicates that at least one of the propositions on either side is true.\n"
        # "   - '&' (AND): Logical conjunction, indicates that both propositions on either side are true.\n"
        # "   - '∀x' (FOR ALL): Universal quantifier, indicates that a statement is true for all values of x.\n"
        # "2. Please refer to the following symbolic reasoning steps and the extracted entities to provide a detailed reasoning explanation in natural language."
        # "For each step, explain in natural language which specific premise or previous inference result is utilized as input, then translate this into its corresponding formal logical expression. Subsequently, declare the exact logical rule applied for the deduction, and finally state the derived conclusion in natural language."
        # #"For each step of reasoning, we provide the given premises and the conclusions that can be deduced. Please explain each step in detail.\n"
        # "3. Then, for each conclusion, refer to the reasoning process generated above and provide an explanation that aligns with the corresponding answer.\n"
        # "4. Finally, Please strictly follow the JSON format below, output the reasoning process and the explanations in the json format:{\"reasoning_process\":[{\"step1\":***,\"explanation\":***},...],\"answer\":{\"conclusion1\":{\"answer\":***,\"explanation\":***},...}} "
        # # f"----example1----\n{example2}"
        # f"####Context:{context}\n"
        # f"####Conclusions: {options}\n" 
        # f"####Entities:{entities}\n"  
        # f"####Reasoning Steps:{reasoning}\n"
        # "##Output:"
# f'''
# You are an expert in Formal Logic and Automated Reasoning. Your task is to interpret symbolic reasoning steps based on a given context and extracted entities to verify specific conclusions.

# ## Input Data Description
# You will be provided with:
# 1. **Context**: The natural language premises.
# 2. **Entities**: Key terms extracted from the context.
# 3. **Reasoning Steps**: A sequence of pre-calculated symbolic logic derivations.
# 4. **Conclusions**: A list of potential conclusions to evaluate (Truth Value: Yes or No).

# ## Logical Symbol Definitions
# - '~' (NOT): Negation (False).
# - '→' (IMPLIES): Implication (If P, then Q).
# - '|' (OR): Disjunction (At least one is True).
# - '&' (AND): Conjunction (Both are True).
# - '∀x' (FOR ALL): Universal Quantifier (True for all x).

# ## Task Instructions

# ### Step 1: Natural Language Reconstruction
# Refer to the provided **Entities** and **Reasoning Steps**. For *each* symbolic step, generate a detailed natural language explanation following this strict structure:
#    - **Source**: Identify which specific premise (from Context) or previous reasoning step is used as input.
#    - **Formalization**: State the symbolic expression being processed.
#    - **Logical Rule**: Declare the specific logic rule applied (e.g., Modus Ponens, Hypothetical Syllogism, De Morgan's Law).
#    - **Derivation**: Translate the resulting symbolic conclusion into a clear, natural language sentence using the corresponding Entities.

# ### Step 2: Conclusion Verification
# Evaluate each option in the **Conclusions** list against your generated reasoning process.
#    - Determine if the conclusion is **Yes** (Strictly follows from the reasoning) or **No** (Does not follow or contradicts).
#    - Provide a brief explanation for your judgment.

# ### Step 3: Final Output
# Output the detailed reasoning process from Step 1 and Step 2, and explicitly state the correct option within \\boxed{{}}.

# ## Input Data
# #### Context:
# {context}

# #### Entities:
# {entities}

# #### Reasoning Steps:
# {reasoning}

# #### Conclusions:
# {options}

# ## Output:
# '''
    )
    return prompt

if __name__ == "__main__":
    filename = sys.argv[1]
    save_file = sys.argv[2]
    data = read_jsonl(filename)
    processed_data = generate_question(data)
    final_data = generate_choice_train_data(processed_data, is_rational=True)
    save_jsonl(final_data, save_file, 'w')