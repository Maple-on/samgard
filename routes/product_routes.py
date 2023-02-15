from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi import UploadFile, File

from services.product_service.product_model import CreateProductModel, UpdateProductModel
from services.product_service.product import create, get_list, get_by_id, delete, update
from database import database

router = APIRouter(
    prefix="/products",
    tags=['Products']
)

get_db = database.get_db


@router.get('/', status_code=status.HTTP_200_OK)
def Get_list(session: Session = Depends(get_db)):
    return get_list(session)


@router.get('/{id}', status_code=status.HTTP_200_OK)
def Get_by_id(id: UUID, session: Session = Depends(get_db)):
    return get_by_id(id, session)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_product(request: CreateProductModel = Depends(), picture: UploadFile = File(...),
                   session: Session = Depends(get_db)):
    return create(request, picture, session)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def Update(id: UUID, request: UpdateProductModel = Depends(), session: Session = Depends(get_db)):
    return update(id, request, session)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def Delete(id: UUID, session: Session = Depends(get_db)):
    return delete(id, session)
