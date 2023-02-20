from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import database
from fastapi.security import OAuth2PasswordRequestForm
from services.auth_service.auth import log_in

router = APIRouter(
    tags=['Authentication']
)

get_db = database.get_db


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    return log_in(request, session)
