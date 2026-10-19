import os

import pandas as pd

# 获取当前文件所在目录（ml）的上一级（也就是项目根目录）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PATH = os.path.join(BASE_DIR, "data", "weather_v1.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "weather_v2.csv")


def clean_data(input_path, output_path):
    print(f"正在清洗数据: {input_path} ...")
    df = pd.read_csv(input_path)

    df['Humidity9am'] = df['Humidity9am'].fillna(df['Humidity9am'].mean())
    df['WindGustDir'] = df['WindGustDir'].fillna(df['WindGustDir'].mode()[0])
    df['WindGustDir'] = df['WindGustDir'].map({'N': 0, 'S': 1, 'E': 2, 'W': 3, 'NE': 4, 'SW': 5})
    df['RainTomorrow'] = df['RainTomorrow'].map({'No': 0, 'Yes': 1})

    df.to_csv(output_path, index=False)
    print(f"✅ 数据清洗完成，保存至 {output_path}")


if __name__ == "__main__":
    clean_data(INPUT_PATH, OUTPUT_PATH)