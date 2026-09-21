from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, get_db
from models import Score as ScoreModel
from schemas.score import Score, Score_update, ScoreResponse

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/scores", response_model=list[ScoreResponse])
def scores(limit: int = Query(5, ge=1, le=5), db: Session = Depends(get_db)):
    return db.query(ScoreModel).limit(limit).all()


@router.post("/scores", response_model=ScoreResponse)
def create_score(score: Score, db: Session = Depends(get_db)):
    existing_score = (db.query(ScoreModel).filter(ScoreModel.name == score.name).first())
    if existing_score:
        raise HTTPException(status_code=409, detail="It already exists")
    new_score = ScoreModel(
        name = score.name,
        rating = score.rating
    )
    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    return new_score
@router.put("/scores/{player_name}", response_model=ScoreResponse)
def update_score(data: Score_update, player_name: str,db: Session = Depends(get_db)):
    player = (
        db.query(ScoreModel)
        .filter(ScoreModel.name == player_name)
        .first()
    )
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    player.rating = data.rating
    db.commit()
    db.refresh(player)
    return player

@router.delete("/scores/{player_name}",response_model=ScoreResponse)
def delete_score(player_name:str, db: Session = Depends(get_db)):
    player = (
            db.query(ScoreModel)
            .filter(ScoreModel.name == player_name)
            .first()
    )
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    db.delete(player)
    db.commit()
    return player