from fastapi import status, Depends, HTTPException, APIRouter
from .. import models, database, oauth2, schemas, utils
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from typing import List

router = APIRouter()


@router.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):

    user_exit = db.query(models.User).filter(models.User.email == user.email).first()

    if user_exit:
        raise HTTPException(status_code=409, detail="email already exists")

    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = oauth2.create_access_token(data={"user_id": new_user.id})
    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "created_at": new_user.created_at,
        "token": token,
    }


@router.post("/login", response_model=schemas.LoginUserResponse)
def login_user(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):

    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials"
        )

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials"
        )

    # create_token

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # tokenData = schemas.Token(access_token=access_token, token_type="bearer")

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "id": user.id,
        "name": user.name,
        "role": user.role,
        "email": user.email,
    }
