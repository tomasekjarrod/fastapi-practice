from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    rating = Column(Float)