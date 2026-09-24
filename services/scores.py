from sqlalchemy.orm import Session
from models import Score as ScoreModel

def get_scores(
    page: int,
    limit: int,
    db: Session,
    min_rating: int | None = None,
    sort: str | None = None,
    order: str = "desc",
    name: str | None = None
):
    query = db.query(ScoreModel)

    if min_rating is not None:
        query = query.filter(ScoreModel.rating >= min_rating)

    if sort == "rating":
        if order == "desc":
            query = query.order_by(ScoreModel.rating.desc())
        else:
            query = query.order_by(ScoreModel.rating.asc())
    if name is not None:
        query = query.filter(
        ScoreModel.name.contains(name)
    )
    total = query.count()

    offset = (page - 1) * limit

    items = query.offset(offset).limit(limit).all()

    return {
        "items": items,
        "page": page,
        "limit": limit,
        "total": total
    }

def create_score(name: str, rating: int, db: Session):
    existing_score = (
        db.query(ScoreModel)
        .filter(ScoreModel.name == name)
        .first()
    )

    if existing_score:
        return None

    new_score = ScoreModel(
        name=name,
        rating=rating
    )

    db.add(new_score)
    db.commit()
    db.refresh(new_score)

    return new_score


def update_score(player_name: str, rating: int, db: Session):
    player = (
        db.query(ScoreModel)
        .filter(ScoreModel.name == player_name)
        .first()
    )

    if not player:
        return None

    player.rating = rating

    db.commit()
    db.refresh(player)

    return player


def delete_score(player_name: str, db: Session):
    player = (
        db.query(ScoreModel)
        .filter(ScoreModel.name == player_name)
        .first()
    )

    if not player:
        return None

    db.delete(player)
    db.commit()

    return player