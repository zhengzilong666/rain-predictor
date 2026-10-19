from pydantic import BaseModel, Field


class WeatherFeatures(BaseModel):
    Rainfall: float = Field(..., ge=0, description="降雨量，必须大于等于0")
    Humidity9am: float = Field(..., ge=0, le=100, description="早上9点湿度，必须在0-100之间")