from typing import List
from pydantic import BaseModel


class APIRequest(BaseModel):
    dtype: str
    shape: List[int]
    image: str


class Face(BaseModel):
    x: int
    y: int
    w: int
    h: int


class APIResponse(BaseModel):
    faces: List[Face]
