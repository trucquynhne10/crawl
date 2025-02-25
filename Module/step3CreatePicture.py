import os
import re
import matplotlib.pyplot as plt
import sys
import pandas as pd
import json
from config.config import CODE_PATH, SAVE_IMAGE_PATH, CODE_JSON, CHART_NAME

def exc_code(MODE):
    no_exec_code = []
    for file_name in os.listdir(CODE_PATH):
        print(file_name)
        if file_name.endswith('.py'):
            file_path = os.path.join(CODE_PATH, file_name)
            file_base = file_name.replace('.py', '')
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                v = fr"{SAVE_IMAGE_PATH}\{file_base}.png"
                if (v not in content):
                    content = content.replace(f"{file_base}.png", f'{v}')

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

            with open(file_path, 'r', encoding='utf-8') as file:
                code = file.read()
            try:
                exec(code)
                print(file_name)
            except Exception as e:
                no_exec_code.append(file_name)
                print(f"Error running {file_name}: {e}")
    file_path = fr'{CODE_JSON}\{CHART_NAME}\{CHART_NAME}_{MODE}.json'
    with open(file_path, 'w') as file:
        json.dump(no_exec_code, file, indent=4)
    print(no_exec_code)
    return no_exec_code

def exc_code_again (no_exec_code, MODE):
    no_exc = []
    for file_name in no_exec_code:
        if file_name.split('.')[0]:
            file_path = os.path.join(CODE_PATH, file_name)            
            with open(file_path, 'r', encoding='utf-8') as file:
                code = file.read()
            try:
                exec(code)
                print(file_name)
            except Exception as e:
                no_exc.append(file_name)
                print(f"Error running {file_name}: {e}")
    file_path = fr'{CODE_JSON}\{CHART_NAME}\{CHART_NAME}_{MODE}.json'
    with open(file_path, 'w') as file:
        json.dump(no_exc, file, indent=4)
    print(no_exec_code)
    return no_exec_code

if __name__ == "__main__":
    MODE = int(sys.argv[1])
    print(MODE)
   
    if MODE == 1: 
        exc_code(MODE)
    elif MODE > 1:
        no_exc = pd.read_json(fr'{CODE_JSON}\{CHART_NAME}\{CHART_NAME}_{MODE - 1}.json')
        print(no_exc[0])
        no_exc = no_exc[0].tolist()
        exc_code_again(no_exc, MODE)



