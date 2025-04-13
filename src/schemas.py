
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


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
