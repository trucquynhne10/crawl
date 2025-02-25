import os
import pandas as pd
from deep_translator import GoogleTranslator
import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display, Markdown
from config.config import CODE_PATH, GOOGLE_API_KEY, MODEL_API_NAME
import time
import re

def translate_code(text, model):
    response = model.generate_content( "dịch các phần nội dung trong code này sang tiếng việt đổi tên save file thành" + file_base_name + "trả kết quả đoạn code " + text + "\n không kèm giải thích gì thêm")
    return response.text

def remove_code_blocks(content):
    # Biểu thức regex để tìm các đoạn từ ``` đến nội dung tiếp theo
    pattern = r"```.*?\n"
    # Thay thế các đoạn tìm được bằng chuỗi rỗng
    return re.sub(pattern, "", content, flags=re.DOTALL)

def to_markdown(text):
    code_blocks = re.findall(r"```.*?```", text, flags=re.DOTALL)
    text_without_code = re.sub(r"```.*?```", "PLACEHOLDER_CODE_BLOCK", text, flags=re.DOTALL)
    text_without_code = text_without_code.replace('•', '  *')
    formatted_text = text_without_code
    for code_block in code_blocks:
        formatted_text = formatted_text.replace("PLACEHOLDER_CODE_BLOCK", code_block, 1)
    return formatted_text
if __name__ == "__main__":
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(MODEL_API_NAME)

    for file_name in os.listdir(CODE_PATH):
        file_path = os.path.join(CODE_PATH, file_name)
        file_base_name = file_name.replace('.py', '')
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            response = translate_code(content, model)
            cleaned_content = remove_code_blocks(response)
            markdown_content = to_markdown(cleaned_content)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(markdown_content)

        print("Đã xong: " + file_base_name)
        time.sleep(3)
