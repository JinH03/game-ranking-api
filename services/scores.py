from sqlalchemy.orm import Session
from models import Score as ScoreModel


def get_scores(limit: int, db: Session):
    return db.query(ScoreModel).limit(limit).all()


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