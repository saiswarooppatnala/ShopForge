from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from database import get_db
from models.user import User
from schemas.user import UserCreate, UserLogin
from auth import create_access_token

router = APIRouter()

password_hash = PasswordHash.recommended()


@router.post("/users")
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    hashed_password = password_hash.hash(user_data.password)

    user = User(
        email=user_data.email,
        password_hash=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "email": user.email
    }


@router.get("/users")
def get_users(
    db: Session = Depends(get_db)
):
    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "email": user.email
        }
        for user in users
    ]


@router.post("/login")
def login_user(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if not user:
        return {"message": "Invalid email or password"}

    password_valid = password_hash.verify(
        user_data.password,
        user.password_hash
    )

    if not password_valid:
        return {"message": "Invalid email or password"}

    access_token = create_access_token(user.id)

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email
    }