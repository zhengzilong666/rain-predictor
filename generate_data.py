import os

import numpy as np
import pandas as pd

os.makedirs("data", exist_ok=True)
np.random.seed(42)  # 保证每次生成的数据一样
num_samples = 1000

# 1. 生成基础特征
min_temp = np.random.uniform(5, 25, num_samples)
max_temp = min_temp + np.random.uniform(5, 15, num_samples)
# 降雨量通常是个长尾分布，大多数时候很小，偶尔暴雨
rainfall = np.random.exponential(5, num_samples)
humidity = np.random.uniform(30, 100, num_samples)
wind_dir = np.random.choice(["N", "S", "E", "W", "NE", "SW"], num_samples)

# 2. 核心：根据物理规律计算下雨的概率
rain_probs = []
for i in range(num_samples):
    prob = 0.05  # 基础概率，就算什么都没发生也有 5% 概率下雨

    # 规律1：早上的湿度越大，下雨概率越高
    if humidity[i] > 80:
        prob += 0.40
    elif humidity[i] > 60:
        prob += 0.15

    # 规律2：当天已经在下大雨了，明天继续下雨的概率极高
    if rainfall[i] > 10.0:
        prob += 0.50
    elif rainfall[i] > 2.0:
        prob += 0.25

    # 规律3：温度骤降也可能伴随降雨
    if max_temp[i] - min_temp[i] < 7:
        prob += 0.10

    rain_probs.append(min(prob, 0.95))  # 概率最高限制在 95%

# 3. 根据算出的概率，生成标签 (Yes/No)
rain_tomorrow = []
for prob in rain_probs:
    if np.random.rand() < prob:
        rain_tomorrow.append("Yes")
    else:
        rain_tomorrow.append("No")

# 4. 组装 DataFrame
data = {
    "MinTemp": min_temp,
    "MaxTemp": max_temp,
    "Rainfall": rainfall,
    "Humidity9am": humidity,
    "WindGustDir": wind_dir,
    "RainTomorrow": rain_tomorrow
}
df = pd.DataFrame(data)

# 5. 故意制造缺失值，为了展示 DVC 数据清洗的价值
df.loc[df.sample(frac=0.1).index, 'Humidity9am'] = np.nan
df.loc[df.sample(frac=0.05).index, 'WindGustDir'] = np.nan

# 保存为 v1
df.to_csv("data/weather_v1.csv", index=False)
print("✅ v1 真实关联数据已生成！明天下雨的比例大概是:", (df['RainTomorrow'] == 'Yes').mean())