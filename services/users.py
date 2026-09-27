from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models import User

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated = "auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(
        plain_password: str,
        hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_user(
        username: str,
        password: str,
        db: Session
):
    existing_user = (db.query(User).filter(User.username == username).first())
    if existing_user: return None
    hashed_password = hash_password(password)
    new_user = User(
        username=username,
        password = hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user