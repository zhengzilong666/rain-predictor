from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_predict_normal():
    """测试1：正常预测 (Happy Path)"""
    payload = {
        "MinTemp": 15.0, "MaxTemp": 25.0, "Rainfall": 0.0, "Humidity9am": 60.0, "WindGustDir": 1
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert response.json()["prediction"] in [0, 1]

def test_predict_missing_field():
    """测试2：缺失字段 (边界条件)"""
    # 故意不传 Humidity9am
    payload = {
        "MinTemp": 15.0, "MaxTemp": 25.0, "Rainfall": 0.0, "WindGustDir": 1
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422 # FastAPI 自动拦截并返回 422

def test_predict_invalid_logic():
    """测试3：非法逻辑数据 (边界条件)"""
    # 湿度不可能超过 100%
    payload = {
        "MinTemp": 15.0, "MaxTemp": 25.0, "Rainfall": 0.0, "Humidity9am": 150.0, "WindGustDir": 1
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422 # Pydantic 校验报错

def test_predict_negative_rainfall():
    """额外测试：降雨量为负数 (边界条件)"""
    payload = {
        "MinTemp": 15.0, "MaxTemp": 25.0, "Rainfall": -5.0, "Humidity9am": 60.0, "WindGustDir": 1
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422