from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class CategoryModel(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class CreateCategoryModel(BaseModel):
    name: str


class UpdateCategoryModel(BaseModel):
    name: Optional[str]
