from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
from uuid import UUID
from datetime import datetime
from sqlalchemy import desc

from services.category_service.category import check_if_category_exists
from services.product_service.bucket import delete_image_from_s3, send_image_to_s3, update_image_from_s3
from services.product_service.product_model import CreateProductModel, UpdateProductModel
from database.models import Product
# from services.order_service.order_model import ProductBase
# from typing import List


def create(request: CreateProductModel, file: UploadFile, db: Session):
    check_if_category_exists(request.category_id, db)
    uploaded_file_url = send_image_to_s3(file)

    new_product = Product(
        name=request.name,
        description=request.description,
        category_id=request.category_id,
        price=request.price,
        quantity=request.quantity,
        unit=request.unit,
        image_url=uploaded_file_url
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


def get_list(offset: int, limit: int, db: Session):
    product = db.query(Product).order_by(desc(Product.created_at)).offset(offset).limit(limit).all()

    return product


def get_by_id(id: UUID, db: Session):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with id {id} not found")

    return product


def update(id: UUID, request: UpdateProductModel, db: Session):
    product = db.get(Product, id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with id {id} not found")
    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == "image_url" and value is not None:
            value = update_image_from_s3(request.image_url, str(product.image_url))
        if value is not None:
            setattr(product, key, value)
    setattr(product, "updated_at", datetime.now())
    db.commit()
    db.refresh(product)

    return product


def delete(id: UUID, db: Session):
    product = db.query(Product).filter(Product.id == id)

    if not product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with id {id} not found")

    file_url = str(product.first().image_url)

    delete_image_from_s3(file_url)
    product.delete(synchronize_session=False)
    db.commit()

    return status.HTTP_204_NO_CONTENT


def check_if_product_exists(product_id: UUID, transaction_quantity: Decimal, db: Session):
    product = db.get(Product, id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with id {id} not found")
    if product.quantity < transaction_quantity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Not enough quantity available")
