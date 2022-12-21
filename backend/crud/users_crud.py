from sqlalchemy.orm import Session

from models import user_model
from schemas.user import UserCreate
from models import user_model
from dependencies import get_password_hash


def get_user(db: Session, id: str) -> user_model.User:
    return db.query(user_model.User).filter(user_model.User.id == id).first()


def get_user_by_email(db: Session, email: str) -> user_model.User:
    return db.query(user_model.User).filter(user_model.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[user_model.User]:
    return db.query(user_model.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> user_model.User:
    hashed_password = get_password_hash(user.password)
    db_user = user_model.User(
        name=user.name,
        surname=user.surname,
        email=user.email,
        hashed_password=hashed_password,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user