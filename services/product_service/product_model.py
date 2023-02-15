from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from fastapi import UploadFile


class ProductModel(BaseModel):
    id: UUID
    name: str
    description: str
    category: UUID
    image: UploadFile
    price: Decimal
    quantity: Decimal
    created_at: datetime
    updated_at: datetime


class CreateProductModel(BaseModel):
    name: str
    description: Optional[str]
    category_id: UUID
    price: Decimal
    quantity: Decimal
    unit: Optional[str]


class UpdateProductModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    category_id: Optional[UUID]
    price: Optional[Decimal]
    quantity: Optional[Decimal]
    unit: Optional[str]
    image_url: Optional[UploadFile]
