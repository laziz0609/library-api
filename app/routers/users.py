from typing import Annotated, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from app.schemas.user import UserRegister, UserResponse
from app.dependencies import get_db
from app.crud.user import get_user_by_username, create_user, get_users
from app.security import hash_password, verify_password, generate_token

router = APIRouter(tags=["users"])

security = HTTPBasic()


@router.post("/api/register", response_model=UserResponse, status_code=201)
async def register_view(
    data: Annotated[UserRegister, Body()],
    db: Annotated[Session, Depends(get_db)],
):
    existing_user = get_user_by_username(db, data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exsists.")

    user = create_user(
        db=db,
        username=data.username,
        hash_password=hash_password(data.password),
    )
    return user


@router.get("/api/users", response_model=List[UserResponse])
async def get_users_view(db: Annotated[Session, Depends(get_db)]):
    return get_users(db)


@router.post("/api/login")
async def login_view(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    db: Annotated[Session, Depends(get_db)],
):
    user = get_user_by_username(db, credentials.username)

    if not user:
        raise HTTPException(status_code=404, detail="user not found.")

    if not verify_password(credentials.password, user.hash_password):
        raise HTTPException(status_code=401, detail="username or password is wrong.")

    token = generate_token({"username": user.username})

    return {"token": token}
