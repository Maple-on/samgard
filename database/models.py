from sqlalchemy import Column, String, UUID, DateTime, ForeignKey, Date, DECIMAL
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
from uuid import uuid4


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID, primary_key=True, default=uuid4)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)


class Category(Base):
    __tablename__ = 'categories'

    id = Column(UUID, primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now)

    product = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = 'products'

    id = Column(UUID, primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category_id = Column(UUID, ForeignKey("categories.id", ondelete="CASCADE"))
    price = Column(DECIMAL, nullable=False)
    quantity = Column(DECIMAL, nullable=False)
    unit = Column(String, default='kg')
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now)

    category = relationship("Category", back_populates="product")
    transaction = relationship("Transaction", back_populates="product")


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(UUID, primary_key=True, default=uuid4)
    product_id = Column(UUID, ForeignKey("products.id", ondelete="CASCADE"))
    quantity = Column(DECIMAL, nullable=False)
    price = Column(DECIMAL, nullable=False)
    payment_method = Column(String, nullable=False)
    status = Column(String, default='pending')
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now)

    product = relationship("Product", back_populates="transaction")
