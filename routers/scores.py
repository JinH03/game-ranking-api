from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from services.scores import get_scores, create_score, update_score, delete_score
from database import get_db
from models import Score as ScoreModel
from schemas.score import Score, Score_update, ScoreResponse

router = APIRouter()
@router.get("/scores", response_model=list[ScoreResponse])
def scores(limit: int = Query(5, ge=1, le=5), db: Session = Depends(get_db)):
    return get_scores(limit, db)


@router.post("/scores", response_model=ScoreResponse)
def create_score_endpoint(
    score: Score,
    db: Session = Depends(get_db)
):
    new_score = create_score(
        score.name,
        score.rating,
        db
    )

    if new_score is None:
        raise HTTPException(
            status_code=409,
            detail="It already exists"
        )

    return new_score

@router.put("/scores/{player_name}", response_model=ScoreResponse)
def update_score_endpoint(
    data: Score_update,
    player_name: str,
    db: Session = Depends(get_db)
):
    player = update_score(
        player_name,
        data.rating,
        db
    )

    if player is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )

    return player


@router.delete("/scores/{player_name}", response_model=ScoreResponse)
def delete_score_endpoint(
    player_name: str,
    db: Session = Depends(get_db)
):
    player = delete_score(player_name, db)

    if player is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )

    return player