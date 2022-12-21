from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str
    email: EmailStr | None = Field(example="email@email.com")
    full_name: str | None = Field(
        default=None, title="User full name", max_length=40, example="Name Surname"
    )
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "user",
                "email": "email@email.com",
                "full_name": "Name Surname",
                "is_active": True,
                "is_superuser": False,
            }
        }


class UserCreate(UserBase):
    password: str = Field(
        title="User password", max_length=40
    )
    confirm_password: str = Field(
        title="Confirm user password", max_length=40
    )

    class Config:
        schema_extra = {
            "example": {
                "email": "email@email.com",
                "password": "Chdo123mFdu@S54",
                "confirm_password": "Chdo123mFdu@S54",
            }
        }


class UserInDB(UserBase):
    hashed_password: str


class UserOut(UserBase):
    pass
