import os

name = os.getenv("CHART_NAME", "rose")

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

OUTPUT_TRANS_DIR = r'D:\Project\NCKH\Module\Translate'
OUTPUT_GOLD_DIR = r'D:\Project\NCKH\Module\GoldMaking'

CSV_FOLDER_PATH = os.getenv("CSV_FOLDER_PATH", fr"D:\Project\NCKH\ChartX\ChartX\{name}\csv")
TXT_FOLDER_PATH = os.getenv("TXT_FOLDER_PATH", fr"D:\Project\NCKH\ChartX\ChartX\{name}\txt")

CHART_NAME = name

GOOGLE_API_KEY = "AIzaSyD0dnoMrLnB4DED5Z8lfVOY1-MftxY6gx8"
MODEL_API_NAME = 'gemini-1.5-flash-002'
LENGTH_PER_TIME = 5

CODE_PATH = fr'D:\Project\NCKH\ChartX\ChartX\{name}\code_using_api'