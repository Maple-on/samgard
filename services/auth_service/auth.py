from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from fastapi.security import OAuth2PasswordRequestForm
from services.auth_service.auth_model import Token
from database.models import User
from database.hashing import Hash
from services.auth_service.token import create_access_token


def log_in(request: OAuth2PasswordRequestForm, db: Session):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Email address")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = create_access_token(data={"sub": user.username})
    token = Token(
        access_token=access_token,
        token_type="bearer"
    )
    return token
