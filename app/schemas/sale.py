import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class SaleItemCreate(BaseModel):
    product_id: uuid.UUID
    quantity: int = Field(..., gt=0)


class SaleCreate(BaseModel):
    items: list[SaleItemCreate] = Field(..., min_length=1)
    notes: str | None = Field(None, max_length=500)


class SaleItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    product_id: uuid.UUID
    quantity: int
    unit_price: Decimal
    subtotal: Decimal


class SaleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: str
    total: Decimal
    sold_by: uuid.UUID | None
    notes: str | None
    sold_at: datetime
    items: list[SaleItemResponse]
    created_at: datetime
