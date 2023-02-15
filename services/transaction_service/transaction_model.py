from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from enum import Enum


class Status(str, Enum):
    pending = "pending"
    paid = "paid"
    cancelled = "cancelled"


class PaymentMethod(str, Enum):
    cash = "cash"
    click = "click"
    payme = "payme"


class TransactionModel(BaseModel):
    id: UUID
    product_id: UUID
    quantity: Decimal
    price: Decimal
    payment_method: PaymentMethod
    status: Status
    created_at: datetime
    updated_at: datetime


class CreateTransactionModel(BaseModel):
    product_id: UUID
    quantity: Decimal
    price: Decimal
    payment_method: PaymentMethod
