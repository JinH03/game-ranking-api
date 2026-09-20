from sqlalchemy import Column, Integer, String
from database import Base

class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    rating = Column(Integer, nullable=False)