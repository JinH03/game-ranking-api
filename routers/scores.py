from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.score import Score, Score_update, ScoreResponse, ScoreListResponse
from services.scores import (
    get_scores,
    create_score,
    update_score,
    delete_score,
)

router = APIRouter()


@router.get(
    "/scores",
    response_model=ScoreListResponse,
    summary="점수 목록 조회",
    description="플레이어 점수를 페이지네이션, 최소 점수 필터, 이름 검색, 정렬 조건과 함께 조회합니다.",
)
def scores(
    page: int = Query(
        1,
        ge=1,
        description="조회할 페이지 번호",
    ),
    limit: int = Query(
        5,
        ge=1,
        le=5,
        description="페이지당 조회할 플레이어 수",
    ),
    db: Session = Depends(get_db),
    min_rating: int | None = Query(
        None,
        ge=0,
        description="조회할 최소 점수",
    ),
    sort: str | None = Query(
        "rating",
        pattern="^(rating)$",
        description="정렬 기준",
    ),
    order: str = Query(
        "desc",
        pattern="^(asc|desc)$",
        description="정렬 방향",
    ),
    name: str | None = Query(
        None,
        description="플레이어 이름 검색",
    ),
):
    return get_scores(
        page,
        limit,
        db,
        min_rating,
        sort,
        order,
        name,
    )


@router.post(
    "/scores",
    response_model=ScoreResponse,
    status_code=201,
    summary="플레이어 점수 등록",
    description="새로운 플레이어와 점수를 등록합니다.",
)
def create_score_endpoint(
    score: Score,
    db: Session = Depends(get_db),
):
    new_score = create_score(
        score.name,
        score.rating,
        db,
    )

    if new_score is None:
        raise HTTPException(
            status_code=409,
            detail="It already exists",
        )

    return new_score


@router.put(
    "/scores/{player_name}",
    response_model=ScoreResponse,
    summary="플레이어 점수 수정",
    description="특정 플레이어의 점수를 수정합니다.",
)
def update_score_endpoint(
    data: Score_update,
    player_name: str,
    db: Session = Depends(get_db),
):
    player = update_score(
        player_name,
        data.rating,
        db,
    )

    if player is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found",
        )

    return player


@router.delete(
    "/scores/{player_name}",
    response_model=ScoreResponse,
    summary="플레이어 삭제",
    description="특정 플레이어의 점수를 삭제합니다.",
)
def delete_score_endpoint(
    player_name: str,
    db: Session = Depends(get_db),
):
    player = delete_score(
        player_name,
        db,
    )

    if player is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found",
        )

    return player 