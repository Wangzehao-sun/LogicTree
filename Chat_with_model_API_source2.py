import os
from sre_constants import SUCCESS
import sys
import json
import time
import shutil
from tkinter.messagebox import RETRY
from token import OP
from turtle import reset
import requests
import threading
import argparse

from tqdm import tqdm
from datetime import datetime, timedelta
from typing import List, Dict, Union, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

##配置
#api配置
API_URL = ""
API_key = "sk-1712.DeXWtaUqHYaQVIKDGLHUn0RiqigpfDAFG1t9kZLOPk5PtrWT"

API_LIST = ["https://wcode.net/api/gpt/v1/chat/completions"]

#请求头
HEADERS = {
    "Content-Type": "application/json",
    #"Accept": "application/json",
    "Authorization": f"Bearer {API_key}"
}

REQUEST_TEMPLATE = {
    "max_tokens": 16384,
    "stream":False,
    # "do_sample":False,
    "temperature": 0.7,
    "top_p":0.8,
    # "top_k":20,
    "model": "qwen/qwen3-235b-a22b-2507",
    "chat_template_kwargs": {
    "enable_thinking":False,
    #   "chat_template": "{%- for message in messages %}{%- if loop.first %}{{ message['content'] }}{%- else %}{{ '\n' + message['content'] }}{%- endif %}{%- endfor %}"
    }
}

# Prompt模板配置
MESSAGES_TEMPLATE = []
SYSTEM_PROMPT = ""
# 输入数据格式 input_text
USER_PROMPT_FORMAT = "{input_txt}"

# 数据处理配置
USER_INPUT_FIELD = "instruction" # 从数据中提取内容的字段
RESPONSE_FIELD = "DeepSeek-R1-answer" # 新增响应字段的名称

# 执行配置
WAIT_TIME = 0 # 脚本等待时间，单位：秒
RETRY_TIMES = 10 #重试次数
TIMEOUT = 1500 # 超时时间（秒）
THREADS = 256 # 并发线程数
STREAM = False # 输出是否使用流式处理

#输入文件配置
INPUTFILE_PATHS = [
    "",
]

OUTPUTFILE_FOLDER = "result"
SUCCESS_OUTPUT_PATH = os.path.join(OUTPUTFILE_FOLDER,"output")
ERROR_OUTPUT_PATH = os.path.join(OUTPUTFILE_FOLDER,"error_out")

# 工具函数
def find_files(
        path: str,
        extensions: Optional[ Union[ str, List[ str ] ] ] = None,
        max_depth: Optional[ int ] = None
        ) -> List[ str ]:
    # 处理后缀参数
    ext_set = set()
    if extensions:
        if isinstance( extensions, str ):
            ext_set.add( extensions.lower() )
        else:
            ext_set = { ext.lower() for ext in extensions}
    
    results = []

    # 栈实现深度限制的遍历，每个元素是（当前路径，当前深度）
    stack = [(os.path.abspath(path),0)]
    while stack:
        current_path, depth = stack.pop()

        if max_depth is not None and depth > max_depth:
            continue

        try:
            with os.scandir(current_path) as entries:
                for entry in entries:
                    if entry.is_file():
                        if not ext_set:
                            results.append(entry.path)
                        else:
                            file_ext = os.path.splitext(entry.name)[1].lower()
                            if file_ext in ext_set:
                                results.append(entry.path)
                    elif entry.is_dir():
                        stack.append((entry.path, depth + 1))
        except PermissionError:
            print(f"警告: 无权限访问目录 {current_path}")
        except FileNotFoundError:
            print(f"警告: 目录不存在 {current_path}")
    return results

def get_file_list(paths:List[str]) -> List[str]:
    """获取要处理的文件列表，支持多个路径"""
    file_list = []
    for path in paths:
        if os.path.isfile(path):
            file_list.append(path)
        elif os.path.isdir(path):
            for f in os.listdir(path):
                if f.endswith((".json",".jsonl")) :
                    file_list.append(os.path.join(path,f))
        else:
            print(f"警告: 路径 {path} 不存在，将被忽略")
    return file_list

def prepare_output_path(input_path,output_base,suffix):
    """根据输入文件路径，生成输出文件路径"""
    if os.path.isdir(output_base):
        filename = f'{os.path.splitext(os.path.basename(input_path))[0]}_{suffix}.json'
        return os.path.join(output_base,filename)
    return output_base


def prepare_output_paths(input_files:List[str]) -> Tuple[List[Tuple[str,str,str]],str,str]:
    """准备输出文件路径"""
    os.makedirs(SUCCESS_OUTPUT_PATH,exist_ok=True)
    os.makedirs(ERROR_OUTPUT_PATH,exist_ok=True)

    # 处理单个文件情况
    if len(input_files) == 1:
        in_file = input_files[0]
        base_name = os.path.basename(in_file)

        if os.path.isdir(SUCCESS_OUTPUT_PATH):
            success_out = prepare_output_path(in_file,SUCCESS_OUTPUT_PATH,"success")
        else:
            success_out = SUCCESS_OUTPUT_PATH
        if os.path.isdir(ERROR_OUTPUT_PATH):
            error_out = prepare_output_path(in_file,ERROR_OUTPUT_PATH,"error")
        else:
            error_out = ERROR_OUTPUT_PATH
        return [(in_file,success_out,error_out)],success_out,error_out
    # 处理多个文件情况
    file_tasks = []
    for in_file in input_files:
        success_out = prepare_output_path(in_file,SUCCESS_OUTPUT_PATH,"success")
        error_out = prepare_output_path(in_file,ERROR_OUTPUT_PATH,"error")
        file_tasks.append((in_file,success_out,error_out))
    return file_tasks, SUCCESS_OUTPUT_PATH, ERROR_OUTPUT_PATH

def delete_if_empty(path):
    """删除空文件"""
    if os.path.exists(path):
        if os.path.isfile(path):
            if os.path.getsize(path) == 0:
                os.remove(path)
                print(f"已删除空文件: {path}")
        elif os.path.isdir(path):
            if not os.listdir(path):
                shutil.rmtree(path)
                print(f"已删除空目录: {path}")
        else:
            print(f"{path} 既不是文件也不是目录，无法删除")
    else:
        print(f"路径 {path} 不存在，无法删除")

def wait_with_progress(seconds):
    """
    带有进度显示的等待函数

    Args:
        seconds (int): 等待的总秒数
    """

    start_time = time.time()
    end_time = start_time + seconds

    print(f"任务等待中 - 总时长：{timedelta(seconds=seconds)}")
    print(f"预计结束时间：{datetime.now() + timedelta(seconds=seconds):%Y-%m-%d %H:%M:%S}\n")

    bar_length = 50  # 进度条长度
    try:
        while time.time() < end_time:
            elapsed = time.time() - start_time
            remaining = end_time - time.time()

            #计算进度百分比
            progress  = min(elapsed / seconds, 1.0)
            filled_length = int(bar_length * progress)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)

            sys.stdout.write(
                f'\r进度: |{bar}| {progress:.1%}'
                f'已等待：{timedelta(seconds=int(elapsed))} '
                f'剩余：{timedelta(seconds=int(remaining))} '
            )
            sys.stdout.flush()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n等待被用户中断")
        elapsed = time.time() - start_time
        print(f"\n等待结束，总共等待时间：{timedelta(seconds=int(elapsed))}\n")
        return False


def process_stream_response(response):
    """
    处理流式响应（SSE格式），实时打印内容并返回完整的响应
    params:
        response: requests.post返回的响应对象
    Returns:
        str: 完整的响应文本
    """
    full_response = ""
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode("utf-8").strip()

            if decoded_line.startswith("data: "):
                data = decoded_line[len("data: "):]
                if data == "[DONE]":
                    break

                try:
                    json_data = json.loads(data)
                    content = json_data['choices'][0]['delta'].get('content','')

                    if content:
                        #print(content, end='', flush=True)
                        full_response += content
                
                except json.JSONDecodeError as e:
                    print(f"\nJSON解析错误: {e},原始数据:{data}")
                except KeyError as e:
                    pass
    return full_response

def single_call_api(data:Dict,retry:int=RETRY_TIMES,stream:bool=STREAM,api_url = API_URL) -> Tuple[bool,Union[str,Dict]]:
    """
    单次调用API
    params:
        data: 请求数据
        retry: 重试次数
        stream: 是否使用流式处理
    Returns:
        Tuple: (是否成功, 响应结果)
    """
    payload = REQUEST_TEMPLATE.copy()

    messages = MESSAGES_TEMPLATE.copy()
    user_content = data.get(USER_INPUT_FIELD,"")
    if not user_content:
        return False, "用户输入内容为空"
    if SYSTEM_PROMPT!="":
        messages.append({"role":"system","content":SYSTEM_PROMPT})
    messages.append({"role":"user","content":USER_PROMPT_FORMAT.format(input_txt=user_content)})

    payload['messages'] = messages

    for attempt in range(retry+1):
        try:
            response = requests.post(
                api_url,
                headers=HEADERS,
                json=payload,
                timeout=TIMEOUT
            )
            #print(response)
            response.raise_for_status()

            if stream:
                result = process_stream_response(response)
                return True, result
            
            result = response.json()
            #print(result)
            if 'choices' in result and len(result['choices']) > 0:
                answer = result['choices'][0]['message']['content']
                return True, answer
            else:
                return False, "API响应格式错误，缺少 'choices' 字段"
        except Exception as e:
            if attempt == retry:
                return False, f"调用API失败: {str(e)}"
            #重试等待-指数退避
            time.sleep((2 ** attempt)*0.1)

    return False,'未知错误'

def process_line(
        data:Dict, success_file:str, error_file:str, 
        success_lock:threading.Lock, error_lock:threading.Lock,api_url = API_URL
)-> Tuple[bool,str]:
    """
    处理单行数据，调用API并写入结果文件
    params:
        data: 输入数据
        success_file: 成功输出文件路径
        error_file: 失败输出文件路径
        success_lock: 成功文件写锁
        error_lock: 失败文件写锁
    Returns:
        Tuple: (是否成功, 消息)
    """
    try:
        success, result = single_call_api(data,api_url=api_url)
        if success:
            data[RESPONSE_FIELD] = result
            with success_lock:
                with open(success_file,'a',encoding='utf-8') as sf:
                    sf.write(json.dumps(data,ensure_ascii=False)+'\n')
            return True, "处理成功"
        else:
            raise Exception(result)
    except Exception as e:
        return False, str(e)
    

#def process_file(

def process_file(input_file:str, success_file:str, error_file:str)-> Dict[str,int]:
    """
    处理单个输入文件，调用API并写入结果文件
    params:
        in_file: 输入文件路径
        success_out: 成功输出文件路径
        error_out: 失败输出文件路径
    """
    
    stats = {"total":0,"success":0,"error":0}

    #准备输出文件
    success_lock = threading.Lock()
    error_lock = threading.Lock()

    #读取输入文件

    try:
        with open(input_file,'r',encoding='utf-8') as inf:
            lines = inf.readlines()
    except Exception as e:
        print(f"错误: 无法读取输入文件 {input_file}: {str(e)}")
        return stats
    
    stats['total'] = len(lines)

    with tqdm(
        total=len(lines),
        desc=f"处理文件: {os.path.basename(input_file)}",
        position=0, #固定位置
        mininterval=0.5, #最小刷新间隔
        maxinterval=1.0,
        dynamic_ncols=True,
        colour="blue",
        leave=True #处理完成后保留进度条
    ) as pbar:
        with ThreadPoolExecutor(max_workers=THREADS) as executor:
            future_to_line = {}

            for idx,line in enumerate(lines):
                remains = idx%len(API_LIST)
                api_url = API_LIST[remains]
                try:
                    data = json.loads(line.strip())
                    future = executor.submit(
                        process_line,
                        data,
                        success_file,
                        error_file,
                        success_lock,
                        error_lock,
                        api_url
                    )
                    future_to_line[future] = (idx,line.strip())
                except json.JSONDecodeError:
                    error_data = {
                        "file":input_file,
                        "line": idx+1,
                        "original": line.strip(),
                        "error":"JSON解析错误"
                    }
                    with error_lock:
                        with open(error_file,'a',encoding='utf-8') as ef:
                            ef.write(json.dumps(error_data,ensure_ascii=False)+'\n')
                    stats['error'] += 1
                    pbar.update(1)
                    pbar.set_postfix({"成功":stats['success'],"失败":stats['error']},refresh=False)
                except Exception as e:
                    error_data = {
                        "file":input_file,
                        "line": idx+1,
                        "original": line.strip(),
                        "error": f"处理错误: {str(e)}"
                    }
                    with error_lock:
                        with open(error_file,'a',encoding='utf-8') as ef:
                            ef.write(json.dumps(error_data,ensure_ascii=False)+'\n')
                    stats['error'] += 1
                    pbar.update(1)
                    pbar.set_postfix({"成功":stats['success'],"失败":stats['error']},refresh=False)

            for future in as_completed(future_to_line):
                idx, original_line = future_to_line[future]
                try:
                    success, error_msg = future.result()
                    if success:
                        stats['success'] += 1
                    else:
                        error_data = {
                            "file":input_file,
                            "line": idx+1,
                            "original": original_line,
                            "error": error_msg
                        }
                        with error_lock:
                            with open(error_file,'a',encoding='utf-8') as ef:
                                ef.write(json.dumps(error_data,ensure_ascii=False)+'\n')
                        stats['error'] += 1
                except Exception as e:
                    error_data = {
                        "file":input_file,
                        "line": idx+1,
                        "original": original_line,
                        "error": f"行处理异常: {str(e)}"
                    }
                    with error_lock:
                        with open(error_file,'a',encoding='utf-8') as ef:
                            ef.write(json.dumps(error_data,ensure_ascii=False)+'\n')
                    stats['error'] += 1
                finally:
                    pbar.update(1)
                    pbar.set_postfix({"成功":stats['success'],"失败":stats['error']},refresh=False)
    return stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfilepaths",
        default=None,
        nargs='+',
        help="输入文件或文件夹路径列表",
    )
    args = parser.parse_args()
    file_paths = args.inputfilepaths if args.inputfilepaths else INPUTFILE_PATHS
    '''主处理函数'''

    print("="*60)
    print("启动API处理任务")
    print(f"API地址列表: {API_LIST}")
    print(f"输入文件列表: ")
    print("\n".join(f"\t{p}" for p in file_paths))
    print(f"成功输出目录: {SUCCESS_OUTPUT_PATH}")
    print(f"失败输出目录: {ERROR_OUTPUT_PATH}")
    print(f"并发线程数: {THREADS}, 重试次数: {RETRY_TIMES}, 超时时间: {TIMEOUT}秒")
    print(f"用户输入字段: '{USER_INPUT_FIELD}'\n输出响应字段: {RESPONSE_FIELD}")
    print("="*60+"\n")


    try:
        input_files = get_file_list(file_paths)
        if not input_files:
            print("错误: 未找到有效的输入文件，程序终止")
            return

        print(f"共找到 {len(input_files)} 个输入文件，准备处理...")
        print("="*60+"\n")
    except Exception as e:
        print(f"错误: 获取输入文件列表失败: {str(e)}")
        return
    
    # 准备输出路径
    file_tasks, success_dir, error_dir = prepare_output_paths(input_files)

    total_stats = {"files":0,"lines":0,"success":0,"error":0}

    for in_file, success_out, error_out in file_tasks:
        total_stats['files'] += 1
        print(f"当前处理文件: {in_file}")
        print(f"当前处理文件个数: {total_stats['files']}")
        print(f"剩余文件个数: {len(file_tasks)-total_stats['files']}")
        print(f"成功数据输出文件: {success_out}")
        print(f"错误数据输出文件: {error_out}")

        for f in [success_out,error_out]:
            if os.path.exists(f):
                os.remove(f)
            open(f,'w',encoding='utf-8').close()
        
        start_time = time.time()
        stats = process_file(in_file,success_out,error_out)
        elapsed = time.time() - start_time

        total_stats['lines'] += stats['total']
        total_stats['success'] += stats['success']
        total_stats['error'] += stats['error']

        #打印文件处理结果

        print(f"\n文件处理完成: {os.path.basename(in_file)}")
        delete_if_empty(error_out)
        print(f"总行数: {stats['total']}, 成功: {stats['success']}, 失败: {stats['error']}")
        print(f"耗时: {elapsed:.2f} 秒, 速度: {stats['total']/max(elapsed,0.1):.1f} 行/秒")
        print("-"*60+"\n")
    #打印最终统计
    print("\n"+"="*60)
    print("所有文件处理完成")
    print(f"总文件数: {total_stats['files']}, 总行数: {total_stats['lines']}, 成功: {total_stats['success']}, 失败: {total_stats['error']}")
    print(f"成功文件位置: {success_dir}")
    print(f"失败文件位置: {error_dir}")
    delete_if_empty(ERROR_OUTPUT_PATH)
    print("="*60+"\n")

if __name__ == "__main__":
    if WAIT_TIME > 0:
        if wait_with_progress(WAIT_TIME):
            print("等待结束，开始处理任务...\n")
            main()
    else:
        main()
