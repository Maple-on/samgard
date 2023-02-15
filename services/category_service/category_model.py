from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

class CategoryModel(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

class CreateCategoryModel(BaseModel):
    name: str

class UpdateCategoryModel(BaseModel):
    name: Optional[str]