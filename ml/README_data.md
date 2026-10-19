# 数据版本控制说明 (DVC)

## 1. 数据来源
本数据集为通过项目中的 `generate_data.py` 脚本模拟生成的澳大利亚天气数据集（Mock Data）。为了模拟真实物理规律，数据生成逻辑中加入了湿度、降雨量对降雨概率的影响权重。

## 2. 数据版本更迭 (v1 -> v2)
- **v1 (原始数据)**: 包含缺失值（如 Humidity9am 存在空值）和文本类别特征（如 WindGustDir）。
- **v2 (清洗数据)**: 在 `data_clean.py` 中进行了数据清洗。使用均值填补了数值型缺失值，使用众数填补了类别型缺失值，并将 `WindGustDir` 映射为 0-5 的数值编码，对目标变量 `RainTomorrow` 进行了 0/1 编码。

## 3. 代码与数据的关联 (Commit Hash 对应关系)
通过 Git 与 DVC 的配合，我们实现了代码与数据的绑定：
- 生成并提交 **v1 数据集** 对应的 Git Commit 为: `feat: initialize project and track v1 raw data with DVC`
- 生成并提交 **v2 数据集** 对应的 Git Commit 为: `feat: create v2 cleaned dataset and track with DVC`
*(通过 Git 历史即可追溯产生特定模型的确切数据版本)*