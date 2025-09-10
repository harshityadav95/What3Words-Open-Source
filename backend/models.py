from sqlalchemy import Column, Integer, String, Float
# Support both package import (backend.*) and direct module import during tests
try:
    from .database import Base
except ImportError:
    from database import Base

class Geocode(Base):
    __tablename__ = "geocodes"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    word1 = Column(String, nullable=False)
    word2 = Column(String, nullable=False)
    word3 = Column(String, nullable=False)