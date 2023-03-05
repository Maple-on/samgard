from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


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
    status: str
    total: Decimal
    payment_id: str
    created_at: datetime
    updated_at: datetime


class CreateOrderDetailsModel(BaseModel):
    client_id: int
    overall_price: Decimal


class OrderItemsModel(BaseModel):
    id: int
    order_id: int
    product_id: int
    amount: Decimal
    product_price: Decimal


class CreateOrderItemsModel(BaseModel):
    order_id: int
    product_id: int
    amount: Decimal
    product_price: Decimal


class CreateOrderItemsModel(BaseModel):
    order_id: int
    product_id: int
    amount: Decimal
    product_price: Decimal


class CreateBaseOrder(BaseModel):
    products: List[ProductBase]
    client_id: int
    total: Decimal
