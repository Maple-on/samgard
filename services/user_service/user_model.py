from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class Role(str, Enum):
    user = "user"
    admin = "admin"
    super_admin = "super_admin"


class UserModel(BaseModel):
    id: UUID
    username: str
    email: str
    password: str
    role: str
    created_at: datetime
    updated_at: datetime


class CreateUserModel(BaseModel):
    username: str
    email: str
    password: str
    role: Role


class UpdateUserModel(BaseModel):
    username: Optional[str]
    password: Optional[str]
    role: Optional[str]
