from pydantic import BaseModel
from typing import Literal

class CoordsRequest(BaseModel):
    latitude: float
    longitude: float
    mode: Literal["global", "india"] = "global"

class WordsRequest(BaseModel):
    word1: str
    word2: str
    word3: str
    mode: Literal["global", "india"] = "global"

class WordsResponse(BaseModel):
    word1: str
    word2: str
    word3: str

class CoordsResponse(BaseModel):
    latitude: float
    longitude: float