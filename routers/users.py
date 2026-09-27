from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.user import UserCreate, UserResponse
from services.users import create_user


router = APIRouter()

@router.post(
    "/users",
    response_model=UserResponse,
    status_code=201
)
def create_user_endpoint(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    new_user = create_user(
        user.username,
        user.password,
        db
    )
    if new_user is None:
        raise HTTPException(status_code=409, detail="Usernmame already exists")
    return new_user