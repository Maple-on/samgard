from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from services.category_service.category_model import CreateCategoryModel, UpdateCategoryModel
from database.models import Category
from datetime import datetime

def create(request: CreateCategoryModel, db: Session):
    new_category = Category(
        name = request.name
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

def get_list(db: Session):
    category = db.query(Category).all()

    return category

def get_by_id(id: UUID, db: Session):
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Category with id {id} not found")

    return category

def update(id: UUID, request: UpdateCategoryModel, db: Session):
    category = db.get(Category, id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with id {id} not found")

    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
            setattr(category, key, value)
    setattr(category, "updated_at", datetime.now())
    db.commit()
    db.refresh(category)

    return category

def delete(id: UUID, db: Session):
    category = db.query(Category).filter(Category.id == id)
    if not category.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Category with id {id} not found")
    
    category.delete(synchronize_session=False)
    db.commit()

    return status.HTTP_204_NO_CONTENT

def check_if_category_exists(id: UUID, db: Session):
    category = db.get(Category, id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with id {id} not found")