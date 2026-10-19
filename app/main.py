from fastapi import FastAPI, HTTPException
from app.schemas import WeatherFeatures
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import joblib
import os
import pandas as pd

app = FastAPI(title="Rain Prediction API")

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html() -> HTMLResponse:
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_js_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.9.0/swagger-ui.css",
    )


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "registry", "current_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"警告: 模型加载失败，请确保已运行 train.py。{e}")


@app.get("/")
def read_root():
    return FileResponse("app/static/index.html")


@app.post("/predict")
def predict_rain(features: WeatherFeatures):
    if model is None:
        raise HTTPException(status_code=500, detail="模型未加载")

    # 【核心修复】强制按照 ["Humidity9am", "Rainfall"] 的顺序构建 DataFrame
    input_data = pd.DataFrame([features.model_dump()])[["Humidity9am", "Rainfall"]]

    prediction = int(model.predict(input_data)[0])

    return {
        "prediction": prediction,
        "description": "明天会下雨 ☔" if prediction == 1 else "明天不会下雨 ☀️"
    }