from typing import List
from pydantic import BaseModel


class ImageSchema(BaseModel):
    dtype: str
    shape: List[int]
    image: str
