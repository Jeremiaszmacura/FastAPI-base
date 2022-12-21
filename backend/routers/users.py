from datetime import datetime, timedelta
from uuid import UUID

from fastapi import APIRouter, Path, HTTPException, Form, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from dependencies import get_current_user, get_current_active_user, authenticate_user, create_access_token
from schemas import user
from schemas.user import UserInDB, UserOut, UserBase
from schemas.token import Token
 
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


fake_users_db = {
    "user1": {
        "username": "user1",
        "email": "email1@email.com",
        "full_name": "Name Surname",
        "is_active": True,
        "is_superuser": False,
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
    },
    "user2": {
        "username": "user2",
        "email": "email1@email.com",
        "full_name": "Name Surname",
        "is_active": True,
        "is_superuser": False,
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
    },
}


def hash_password(raw_password: str):
    # TODO
    return raw_password


@token_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login/", response_model=UserOut)
async def login(
    email: str = Form(title="User email", min_length=6, max_length=40),
    password: str = Form(title="User password", max_length=40)
    ):
    return {"username": email, "password": password}


@router.get("/", response_model=list[UserOut])
async def read_users():
    return fake_users_db


@router.get("/me")
async def read_users_me(current_user: UserBase = Depends(get_current_active_user)):
    return current_user


@router.get("/{user_id}", response_model=UserOut)
async def read_user(user_id: UUID = Path(title="The ID of the item to get")):
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": fake_users_db[user_id]["username"], "item_id": user_id}


@router.post("/", status_code=201, response_model=UserOut)
async def create_user(
    email: str = Form(title="User email", in_length=6, max_length=40),
    full_name: str = Form(title="User full name", max_length=40),
    password: str = Form(title="User password", max_length=40),
    confirm_password: str = Form(title="Confirm user password", max_length=40)
    ):
    print(email, full_name, password, confirm_password)
    return {"username": fake_users_db["1"]["username"], "item_id": "1"}
