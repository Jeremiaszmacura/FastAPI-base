from uuid import UUID

from fastapi import APIRouter, Path, HTTPException, Form, Depends
from fastapi.security import OAuth2PasswordRequestForm
from dependencies import get_current_user

from schemas import user
from schemas.user import UserInDB

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


fake_users_db = {
    "user1": {
        "username": "user1",
        "email": "email1@email.com",
        "full_name": "Name Surname",
        "is_active": True,
        "is_superuser": False,
        "hashed_password": "password"
    },
    "user2": {
        "username": "user2",
        "email": "email1@email.com",
        "full_name": "Name Surname",
        "is_active": True,
        "is_superuser": False,
        "hashed_password": "password"
    },
}


def hash_password(raw_password: str):
    # TODO
    return raw_password


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(fake_users_db.get(form_data.username))
    print(form_data)
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@router.post("/login/", response_model=user.UserOut)
async def login(
    email: str = Form(title="User email", min_length=6, max_length=40),
    password: str = Form(title="User password", max_length=40)
    ):
    return {"username": email, "password": password}


# @router.get("/token/")
# async def read_items(current_user: user.UserBase = Depends(get_current_user)):
#     return {"current_user": current_user}


# @router.get("/", response_model=list[user.UserOut])
# async def read_users(
#     current_user: models.User = Depends(deps.get_current_active_superuser)
# ):
#     return fake_users_db


@router.get("/", response_model=list[user.UserOut])
async def read_users():
    return fake_users_db


@router.get("/{user_id}", response_model=user.UserOut)
async def read_user(user_id: UUID = Path(title="The ID of the item to get")):
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": fake_users_db[user_id]["username"], "item_id": user_id}


@router.post("/", status_code=201, response_model=user.UserOut)
async def create_user(
    email: str = Form(title="User email", in_length=6, max_length=40),
    full_name: str = Form(title="User full name", max_length=40),
    password: str = Form(title="User password", max_length=40),
    confirm_password: str = Form(title="Confirm user password", max_length=40)
    ):
    print(email, full_name, password, confirm_password)
    return {"username": fake_users_db["1"]["username"], "item_id": "1"}
