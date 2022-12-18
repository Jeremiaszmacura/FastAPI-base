from pydantic import BaseModel, EmailStr, Field, validator


class UserBase(BaseModel):
    email: EmailStr | None = Field(example="email@email.com")
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    full_name: str | None = Field(
        default=None, title="User full name", max_length=40, example="Name Surname"
    )

    class Config:
        schema_extra = {
            "example": {
                "email": "email@email.com",
                "is_active": True,
                "is_superuser": False,
                "full_name": "Name Surname",
            }
        }

    @validator('full_name')
    def name_must_contain_space(cls, v):
        assert v.isalnum(), 'Full name must be alphanumeric'
        if ' ' not in v:
            raise ValueError('Full name must contain a space')
        return v.title()


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
