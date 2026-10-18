import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, accuracy_score
import joblib
import os

# 1. 设置 MLflow 实验名
mlflow.set_experiment("Rain_Prediction_Experiments")

# 动态获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def train_model(data_path, n_estimators, max_depth, run_name):
    full_path = os.path.join(BASE_DIR, data_path)
    # 加载数据
    df = pd.read_csv(full_path)

    # 【新增修复代码】检查如果有文本列，统一转换为数字，防止模型报错
    if df['WindGustDir'].dtype == 'object':
        df['WindGustDir'] = df['WindGustDir'].map({'N': 0, 'S': 1, 'E': 2, 'W': 3, 'NE': 4, 'SW': 5}).fillna(0)
    if df['RainTomorrow'].dtype == 'object':
        df['RainTomorrow'] = df['RainTomorrow'].map({'No': 0, 'Yes': 1})

    X = df.drop("RainTomorrow", axis=1)
    y = df["RainTomorrow"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    with mlflow.start_run(run_name=run_name):
        # 训练模型
        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
        model.fit(X_train, y_train)

        # 预测与评估
        preds = model.predict(X_test)
        f1 = f1_score(y_test, preds)
        acc = accuracy_score(y_test, preds)

        # 记录到 MLflow
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("accuracy", acc)

        print(f"[{run_name}] F1 Score: {f1:.4f}, Accuracy: {acc:.4f}")

        # 将表现更好的模型保存下来供 API 使用
        registry_dir = os.path.join(BASE_DIR, "ml", "registry")
        os.makedirs(registry_dir, exist_ok=True)
        if run_name == "Improved_Model":
            model_path = os.path.join(registry_dir, "current_model.pkl")
            joblib.dump(model, model_path)
            print(f"✅ 生产模型已保存至 {model_path}")


if __name__ == "__main__":
    # 实验 1：Baseline（用 v1 数据，参数简单）
    train_model("data/weather_v1.csv", n_estimators=10, max_depth=3, run_name="Baseline_Model")

    # 实验 2：Improved（用 v2 清洗数据，参数更复杂）
    train_model("data/weather_v2.csv", n_estimators=50, max_depth=10, run_name="Improved_Model")