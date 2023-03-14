from enum import Enum
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class OrderStatus(str, Enum):
    new = "New"
    completed = "Completed"
    cancelled = "Cancelled"


class ProductBase(BaseModel):
    id: int
    amount: Decimal


class ProductForWithdraw(BaseModel):
    id: int
    name: str
    amount: Decimal
    price: Decimal
    amount_to_withdraw: Optional[Decimal]


class OrderDetailsModel(BaseModel):
    id: int
    client_id: int
    order_status: OrderStatus
    total: Decimal
    payment_status: str
    payment_id: str
    created_at: datetime
    updated_at: datetime


class CreateBaseOrder(BaseModel):
    products: List[ProductBase]
    client_id: int
    total: Decimal
