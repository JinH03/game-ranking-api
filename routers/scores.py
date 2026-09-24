from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Score as ScoreModel
from schemas.score import Score, Score_update, ScoreResponse, ScoreListResponse
from services.scores import get_scores, create_score, update_score, delete_score
router = APIRouter()

@router.get("/scores", response_model=ScoreListResponse)
def scores(
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1, le=5),
    db: Session = Depends(get_db),
    min_rating: int | None = Query(None, ge=0),
    sort: str | None = Query("rating", pattern="^(rating)$"),
    order: str = Query("desc", pattern="^(asc|desc)$"),
    name: str | None = Query(None)
):
    return get_scores(
        page,
        limit,
        db,
        min_rating,
        sort,
        order,
        name
    )
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