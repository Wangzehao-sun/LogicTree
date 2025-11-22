import json
import random
import os

outdir = "temp/example_each_format"

# with open("final/data_choice.jsonl",'r',encoding='utf-8') as f:
#     lines = f.readlines()

# samplelines = random.sample(lines, 100)
# sampledata = []
# for i,line in enumerate(samplelines,1):
#     try:
#         data = json.loads(line.strip())
#         sampledata.append(data)
#     except Exception as e:
#         print(e)
# with open("temp/example_each_format/QA.jsonl",'w',encoding='utf-8') as f:
#     for data in sampledata:
#         f.write(json.dumps(data, ensure_ascii=False) + '\n')

with open("final/data_1116_1_train_story.jsonl",'r',encoding='utf-8') as f:
    lines = f.readlines()

format_list = ["educ","news","wiki","blog","stor","maga","abst","tech"]
for format in format_list:
    count = 0
    results = []
    while count<500:
        line = random.sample(lines, 1)[0]
        try:
            data = json.loads(line.strip())
            if data["format"] == format:
                results.append(data)
                count += 1
        except Exception as e:
            print(e)
    with open(os.path.join(outdir,f"{format}.jsonl"),'w',encoding='utf-8') as f:
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')
    