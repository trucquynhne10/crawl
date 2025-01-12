import os
import pandas as pd
from deep_translator import GoogleTranslator
import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display, Markdown
from config.config import CSV_FOLDER_PATH, TXT_FOLDER_PATH, CHART_NAME, GOOGLE_API_KEY, MODEL_API_NAME, LENGTH_PER_TIME
import time

def translate_text(text, translator):
    return translator.translate(text)

def translate(df, source_lang='en', target_lang='vi'):
    translator = GoogleTranslator(source=source_lang, target=target_lang)
    df['Translated_Data'] = df['Data'].astype(str).apply(lambda x: translate_text(x, translator))
    df['Translated_Title'] = df['Title'].astype(str).apply(lambda x: translate_text(x, translator))
    return df

def making_gold(df, model, LENGTH_PER_TIME, delay=5):  # Delay mặc định là 5 giây
    for i in range(LENGTH_PER_TIME):
        response = model.generate_content(
            "Viết đoạn mô tả phân tích biểu đồ ngắn gọn từ 4 5 câu dựa trên số liệu này" + df['Translated_Data'].iloc[i] + " theo tên biểu đồ là" + df['Translated_Title'].iloc[i]
        )
        content = response.text
        df['Gold'].iloc[i] = content
        print(i)
        
        # Thêm thời gian chờ giữa các yêu cầu
        time.sleep(delay)  # Điều chỉnh delay tùy theo nhu cầu

    return df

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

if __name__ == "__main__":
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(MODEL_API_NAME)

    chart_types = [
    "treemap",
    "radar",
    "rings",
    "multi-axes",
    "histogram",
    "funnel",
    "heatmap",
    "box",
    "bubble",
    "candlestick",
    "bar_chart_num"
    ]

    for name in range(2):
        final_data = pd.read_csv(f'Translate/{chart_types[name]}_trans_json.csv')
        if os.path.isdir(CSV_FOLDER_PATH) and os.path.isdir(TXT_FOLDER_PATH):
            if final_data is not None:
                output_gold_dir = "GoldMaking"
                final_data['Gold'] = None
                final_gold_data = making_gold(final_data, model, len(final_data))
                print(final_gold_data)
                final_gold_data.to_csv(os.path.join(output_gold_dir, f"{CHART_NAME}_gold.csv"), encoding='utf-8-sig', index=False)
                print("Dữ liệu đã được lưu tại các thư mục tương ứng.")
        else:
            print("Đường dẫn trong config.py không hợp lệ. Vui lòng kiểm tra lại.")
