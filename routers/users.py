from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from services.auth import create_access_token, decode_access_token
from database import get_db
from schemas.user import UserCreate, UserResponse, Token
from services.users import create_user, login_user


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    username = payload.get("sub")

    if username is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return username


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
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )

    return new_user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = login_user(
        form_data.username,
        form_data.password,
        db
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        {"sub": user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me")
def get_me(
    current_user: str = Depends(get_current_user)
):
    return {
        "username": current_user
    }