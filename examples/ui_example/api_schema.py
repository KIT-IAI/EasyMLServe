from typing import List
from pydantic import BaseModel


class APIRequest(BaseModel):
    dtype: str
    shape: List[int]
    image: str
    bins: int


class Histogram(BaseModel):
    counts: List[int]
    rel_counts: List[float]
    bins: List[float]


class APIResponse(BaseModel):
    shape: List[int]
    r: Histogram
    g: Histogram
    b: Histogram
