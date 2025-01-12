import os
import pandas as pd
from deep_translator import GoogleTranslator
import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display, Markdown
from config.config import CSV_FOLDER_PATH, TXT_FOLDER_PATH, CHART_NAME, GOOGLE_API_KEY, MODEL_API_NAME, LENGTH_PER_TIME
import time

def process_files(csv_folder_path=CSV_FOLDER_PATH, txt_folder_path=TXT_FOLDER_PATH):
    all_data_js = []

    for file_name in os.listdir(csv_folder_path):
        if file_name.endswith('.csv'): 
            file_path = os.path.join(csv_folder_path, file_name)
            try:
                df = pd.read_csv(file_path)
                flat_list_js = df.to_json(orient='records')
            except Exception as e:
                print(f"Lỗi khi đọc file {file_name}: {e}")
                continue

            txt_file_name = file_name.replace('.csv', '.txt')
            txt_file_path = os.path.join(txt_folder_path, txt_file_name)

            if os.path.exists(txt_file_path):
                try:
                    with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
                        title_value = txt_file.read().strip()
                except Exception as e:
                    print(f"Lỗi khi đọc file {txt_file_name}: {e}")
                    title_value = "No Title"
            else:
                title_value = "No Title"

            all_data_js.append({
                'File': file_name.replace(".csv", ""),  
                'Title': title_value,
                'Data': flat_list_js
            })

    try:
        df_final_js = pd.DataFrame(all_data_js)
        print("Dữ liệu cuối cùng đã được xử lý thành công.")
        return df_final_js
    except Exception as e:
        print(f"Lỗi khi tạo DataFrame cuối cùng: {e}")
        return None

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

    if os.path.isdir(CSV_FOLDER_PATH) and os.path.isdir(TXT_FOLDER_PATH):
        final_data = process_files(CSV_FOLDER_PATH, TXT_FOLDER_PATH)
        if final_data is not None:
            final_data = translate(final_data)
            output_tran_dir = "Translate"
            output_gold_dir = "GoldMaking"
            os.makedirs(output_gold_dir, exist_ok=True)
            # final_data['Gold'] = None
            # final_gold_data = making_gold(final_data, model, LENGTH_PER_TIME)
            # print(final_gold_data)
            final_data.to_csv(os.path.join(output_tran_dir, f"{CHART_NAME}_trans_json.csv"), encoding='utf-8-sig', index=False)
            # final_gold_data.to_csv(os.path.join(output_gold_dir, f"{CHART_NAME}_gold.csv"), encoding='utf-8-sig', index=False)
            
            print("Dữ liệu đã được lưu tại các thư mục tương ứng.")
    else:
        print("Đường dẫn trong config.py không hợp lệ. Vui lòng kiểm tra lại.")
