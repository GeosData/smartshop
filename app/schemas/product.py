import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    sku: str | None = Field(None, max_length=50)
    description: str | None = None
    price: Decimal = Field(..., gt=0, decimal_places=2)
    cost: Decimal | None = Field(None, ge=0, decimal_places=2)
    stock: int = Field(default=0, ge=0)
    min_stock: int = Field(default=5, ge=0)
    category: str | None = Field(None, max_length=100)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=200)
    sku: str | None = Field(None, max_length=50)
    description: str | None = None
    price: Decimal | None = Field(None, gt=0, decimal_places=2)
    cost: Decimal | None = Field(None, ge=0, decimal_places=2)
    stock: int | None = Field(None, ge=0)
    min_stock: int | None = Field(None, ge=0)
    category: str | None = Field(None, max_length=100)
    is_active: bool | None = None


class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: str
    is_active: bool
    is_low_stock: bool
    created_at: datetime
    updated_at: datetime


class ProductList(BaseModel):
    items: list[ProductResponse]
    total: int
    page: int
    page_size: int
