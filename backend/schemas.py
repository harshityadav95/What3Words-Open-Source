from pydantic import BaseModel

class CoordsRequest(BaseModel):
    latitude: float
    longitude: float

class WordsRequest(BaseModel):
    word1: str
    word2: str
    word3: str

class WordsResponse(BaseModel):
    word1: str
    word2: str
    word3: str

class CoordsResponse(BaseModel):
    latitude: float
    longitude: float