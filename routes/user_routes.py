from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from services.user_service.user_model import CreateUserModel, UpdateUserModel
from services.user_service.user import create, get_list, get_by_id, delete, update
from services.user_service.user_model import UserModel
from database import database

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

get_db = database.get_db


@router.get('/', status_code=status.HTTP_200_OK)
def Get_list(session: Session = Depends(get_db)):
    return get_list(session)


# get, post, put, delete methods are working but disabled for security purposes for now

# @router.get('/{id}', status_code=status.HTTP_200_OK)
# def Get_by_id(id: UUID, session: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
#     return get_by_id(id, session)

@router.post('/', status_code=status.HTTP_201_CREATED)
def Create(request: CreateUserModel, session: Session = Depends(get_db)):
    return create(request, session)

# @router.put('/{id}', status_code=status.HTTP_202_ACCEPTED) def Update(id: UUID, request: UpdateUserModel,
# session: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)): return update(id,
# request, session)

# @router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def Delete(id: UUID, session: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
#     return delete(id, session)
