from fastapi import status, Depends, HTTPException, Response, APIRouter
from .. import models, database, schemas, utils, oauth2

from sqlalchemy.orm import Session
from typing import List

from ..schemas import User

router = APIRouter()


@router.get("/", response_model=List[schemas.UserResponse])
def get_users(
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    users = db.query(models.User).all()
    return users


@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: schemas.User = Depends(oauth2.get_current_user)):

    return current_user


@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id : {user_id} not found",
        )

    return user


@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(database.get_db),
):
    user_query = db.query(models.User).filter(models.User.id == user_id)
    user = user_query.first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id : {user_id} not found",
        )

    user_query.update(user_update.model_dump(), synchronize_session=False)
    db.commit()

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(oauth2.get_current_user),
):
    user_query = db.query(models.User).filter(models.User.id == user_id)

    if user_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id : {user_id} was not found",
        )
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
