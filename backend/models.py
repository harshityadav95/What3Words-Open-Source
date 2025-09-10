from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Geocode(Base):
    __tablename__ = "geocodes"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    word1 = Column(String, nullable=False)
    word2 = Column(String, nullable=False)
    word3 = Column(String, nullable=False)