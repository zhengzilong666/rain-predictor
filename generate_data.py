import pandas as pd
import numpy as np
import os

# 确保 data 文件夹存在
os.makedirs("data", exist_ok=True)

# 模拟 1000 条天气数据
np.random.seed(42)
data = {
    "MinTemp": np.random.uniform(0, 20, 1000),
    "MaxTemp": np.random.uniform(15, 40, 1000),
    "Rainfall": np.random.exponential(2, 1000),
    "Humidity9am": np.random.uniform(20, 100, 1000),
    "WindGustDir": np.random.choice(["N", "S", "E", "W", "NE", "SW"], 1000),
    "RainTomorrow": np.random.choice(["Yes", "No"], 1000, p=[0.2, 0.8]) # 预测目标
}
df = pd.DataFrame(data)

# 故意制造一些缺失值 (模拟 v1 原始脏数据)
df.loc[df.sample(frac=0.1).index, 'Humidity9am'] = np.nan
df.loc[df.sample(frac=0.05).index, 'WindGustDir'] = np.nan

# 保存为原始数据 v1
df.to_csv("data/weather_v1.csv", index=False)
print("✅ v1 原始数据已成功生成: data/weather_v1.csv")