from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from fastapi import UploadFile


class ProductModel(BaseModel):
    id: int
    name: str
    description: str
    category: int
    image: UploadFile
    price: Decimal
    amount: Decimal
    created_at: datetime
    updated_at: datetime


class CreateProductModel(BaseModel):
    name: str
    description: Optional[str]
    category_id: int
    price: Decimal
    amount: Decimal
    unit: Optional[str]


class UpdateProductModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    category_id: Optional[int]
    price: Optional[Decimal]
    amount: Optional[Decimal]
    unit: Optional[str]
    image_url: Optional[UploadFile]
