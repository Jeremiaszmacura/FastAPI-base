from uuid import UUID

from fastapi import APIRouter, Path, Depends, HTTPException

from dependencies import get_token_header
from schemas import user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


fake_users_db = {"1": {"username": "Rick"}, "2": {"username": "Morty"}}


def hash_password(raw_password: str):
    # TODO
    return raw_password


@router.get("/", response_model=list[user.UserOut])
async def read_users():
    return fake_users_db


@router.get("/{user_id}", response_model=user.UserOut)
async def read_user(user_id: UUID = Path(title="The ID of the item to get")):
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": fake_users_db[user_id]["username"], "item_id": user_id}


@router.post("/", status_code=201, response_model=user.UserOut)
async def create_user(user: user.UserCreate):
    print(user)
    return {"username": fake_users_db["1"]["username"], "item_id": "1"}
