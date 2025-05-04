
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


class PaginationParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["id", "created_at", "updated_at"] = "id"
    sort: Literal["asc", "desc"] = "asc"


class PartFilters(PaginationParams):
    order_by: Literal["id", "price", "quantity", "created_at", "updated_at"] = "id"

    part_number: str | None = Field(default=None)
    description: str | None = Field(default=None)
    quantity: int | None = Field(default=None, ge=0)


class PartBase(BaseModel):
    part_number: str
    description: str | None = None
    price: float = Field(..., ge=0)
    quantity: int = Field(..., ge=0)


class PartCreate(PartBase):
    pass


class PartResponse(PartBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime | None = None
