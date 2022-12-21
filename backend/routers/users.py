from datetime import timedelta
from typing import Any

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from crud import users_crud
from dependencies import get_current_active_user, authenticate_user, create_access_token
from schemas.user import UserOut, UserCreate
from models.user_model import User
from schemas.token import Token
from database import get_db
 
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

token_router = APIRouter(
    tags=["token"],
    responses={404: {"description": "Not found"}},
)


@token_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Any:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=UserOut)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Any:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/", response_model=list[UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> Any:
    users = users_crud.get_users(db, skip=skip, limit=limit)
    users = list(UserOut(**user.__dict__) for user in users)
    return users


@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_active_user)) -> Any:
    current_user = UserOut(**current_user.__dict__)
    return current_user


@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)) -> Any:
    db_user = users_crud.get_user_by_email(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/", status_code=201, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> Any:
    db_user = users_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = users_crud.create_user(db=db, user=user)
    return UserOut(**user.__dict__)
