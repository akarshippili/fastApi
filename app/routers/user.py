from ..schemas import UserCreate, UserResponse
from .. import models, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=201, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # hashing password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    # creating new user and inserting into db
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return user
