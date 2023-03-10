from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
from datetime import datetime
from sqlalchemy import desc, text, func

from services.category_service.category import check_if_category_exists
from services.product_service.bucket import delete_image_from_s3, send_image_to_s3, update_image_from_s3
from services.product_service.product_model import CreateProductModel, UpdateProductModel
from database.models import Product, Category
from services.order_service.order_model import ProductBase, ProductForWithdraw
from typing import List


def create(request: CreateProductModel, file: UploadFile, db: Session):
    check_if_category_exists(request.category_id, db)
    uploaded_file_url = send_image_to_s3(file)

    new_product = Product(
        name=request.name,
        description=request.description,
        category_id=request.category_id,
        price=request.price,
        amount=request.amount,
        unit=request.unit,
        image_url=uploaded_file_url
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    db.close()

    return new_product


def get_list(offset: int, limit: int, category_id: int, db: Session):
    sql = "SELECT COUNT(*) FROM products"
    count = db.execute(text(sql)).fetchone()[0]
    products = db.query(Product, Category.name).join(Category, Product.category_id == Category.id).order_by(desc(Product.created_at))

    if category_id != 0:
        products = products.filter(Product.category_id == category_id)

    products = products.offset(offset).limit(limit).all()

    product_list = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "category_id": product.category_id,
            "category_name": category_name,
            "price": product.price,
            "amount": product.amount,
            "unit": product.unit,
            "image_url": product.image_url,
            "created_at": product.created_at,
            "updated_at": product.updated_at
        }
        for product, category_name in products
    ]
    db.close()

    return {"products": product_list, "total": count}


def get_by_id(id: int, db: Session):
    result = db.query(Product, Category.name).join(Category, Product.category_id == Category.id).filter(Product.id == id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with id {id} not found")
    product = result[0]
    category_name = result[1]
    product_list = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "category_id": product.category_id,
        "category_name": category_name,
        "price": product.price,
        "amount": product.amount,
        "unit": product.unit,
        "image_url": product.image_url,
        "created_at": product.created_at,
        "updated_at": product.updated_at
    }
    db.close()

    return product_list


def update(id: int, request: UpdateProductModel, db: Session):
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
    db.close()

    return product


def delete(id: int, db: Session):
    product = db.query(Product).filter(Product.id == id)

    if not product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with id {id} not found")

    file_url = str(product.first().image_url)

    delete_image_from_s3(file_url)
    product.delete(synchronize_session=False)
    db.commit()
    db.close()

    return status.HTTP_204_NO_CONTENT


def check_if_product_exists(product_list: List[ProductBase], db: Session):
    ids = {str(product.id) for product in product_list}

    sql = "SELECT COUNT(*) FROM products WHERE id IN :ids"
    count = db.execute(text(sql), {"ids": tuple(ids)}).fetchone()[0]
    db.close()

    if count != len(ids):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"At least one of products is not found")


def check_products_amount_and_return_data(product_list: List[ProductBase], db: Session):
    ids = {str(product.id) for product in product_list}

    sql = "SELECT id, name, amount, price FROM products WHERE id IN :ids"
    products = db.execute(text(sql), {"ids": tuple(ids)}).fetchall()
    db.close()

    db_product_list = [ProductForWithdraw(id=id, name=name, amount=amount, price=price) for id, name, amount, price in products]

    for user_product in product_list:
        for db_product in db_product_list:
            if user_product.id == db_product.id:
                if user_product.amount > db_product.amount:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f"Not enough amount of product('{db_product.name}') with id('{db_product.id}')")
                else:
                    db_product.amount_to_withdraw = user_product.amount
    return db_product_list


def update_product_amount(id: int, amount_to_withdraw: Decimal, db: Session):
    sql = f"UPDATE products SET amount = amount - {amount_to_withdraw} WHERE id = '{id}'"
    db.execute(text(sql))
