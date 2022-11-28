from typing import List
from pydantic import BaseModel


class APIRequest(BaseModel):
    models: List[str]
    time: List[str]
    energy: List[float]


class Forecast(BaseModel):
    model: str
    time: List[str]
    energy: List[float]


class APIResponse(BaseModel):
    forecasts: List[Forecast]
