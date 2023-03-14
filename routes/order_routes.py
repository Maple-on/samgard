from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from services.order_service.order_model import CreateBaseOrder
from services.order_service.order import create, get_list, get_by_id, delete, cancel
from database import database

router = APIRouter(
    prefix="/orders",
    tags=['Orders']
)

get_db = database.get_db


@router.get('/', status_code=status.HTTP_200_OK)
def Get_list(offset: int = 0, limit: int = 10, session: Session = Depends(get_db)):
    return get_list(offset, limit, session)


@router.get('/{id}', status_code=status.HTTP_200_OK)
def Get_by_id(id: int, session: Session = Depends(get_db)):
    return get_by_id(id, session)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_order(request: CreateBaseOrder, session: Session = Depends(get_db)):
    return create(request, session)


# @router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
# def Update(id: UUID, request: UpdateProductModel = Depends(), session: Session = Depends(get_db)):
#     return update(id, request, session)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def Delete(id: int, session: Session = Depends(get_db)):
    return delete(id, session)


@router.post('/cancel/{id}', status_code=status.HTTP_202_ACCEPTED)
def Cancel(id: int, session: Session = Depends(get_db)):
    return cancel(id, session)
