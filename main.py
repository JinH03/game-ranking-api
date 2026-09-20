from fastapi import FastAPI, Path
from fastapi import HTTPException, Query
from pydantic import BaseModel, Field
from routers.scores import router as score_router
from database import Base, engine
import models

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(score_router)




##uvicorn main:app --reload
