from pydantic import BaseModel, Field

class WeatherFeatures(BaseModel):
    MinTemp: float = Field(..., description="最低温度")
    MaxTemp: float = Field(..., description="最高温度")
    Rainfall: float = Field(..., ge=0, description="降雨量，必须大于等于0")
    Humidity9am: float = Field(..., ge=0, le=100, description="早上9点湿度，必须在0-100之间")
    WindGustDir: int = Field(..., ge=0, le=5, description="风向编码 0-5")