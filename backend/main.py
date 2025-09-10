from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Support running as a package (uvicorn backend.main:app) and as a module in tests (pytest from backend/)
try:
    from .database import SessionLocal, engine
    from . import models
    from .schemas import CoordsRequest, WordsRequest, WordsResponse, CoordsResponse
    from .geocoding import lat_lng_to_words, words_to_lat_lng
except ImportError:
    # Fallback for direct execution/import without package context
    from database import SessionLocal, engine
    import models
    from schemas import CoordsRequest, WordsRequest, WordsResponse, CoordsResponse
    from geocoding import lat_lng_to_words, words_to_lat_lng

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="What3Words Clone API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# The CORSMiddleware will handle OPTIONS requests automatically.
# Explicitly defining them can sometimes cause issues.
# @app.options("/convert-coords")
# def options_convert_coords():
#     return {"message": "OK"}
#
# @app.options("/convert-words")
# def options_convert_words():
#     return {"message": "OK"}

@app.post("/convert-coords", response_model=WordsResponse)
def convert_coords_to_words(request: CoordsRequest):
    """Convert latitude and longitude to three words"""
    try:
        word1, word2, word3 = lat_lng_to_words(request.latitude, request.longitude, request.mode)
        return WordsResponse(word1=word1, word2=word2, word3=word3)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/convert-words", response_model=CoordsResponse)
def convert_words_to_coords(request: WordsRequest):
    """Convert three words to latitude and longitude"""
    try:
        lat, lng = words_to_lat_lng(request.word1, request.word2, request.word3, request.mode)
        return CoordsResponse(latitude=lat, longitude=lng)
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid words provided")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "What3Words Clone API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)