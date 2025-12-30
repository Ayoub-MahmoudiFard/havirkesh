from pydantic import BaseModel as PydanticBase
from datetime import datetime

from pydantic import Field
from typing import Optional

from decimal import Decimal

class FactorySeedCreate(PydanticBase):
    factory_id: int
    seed_id: int
    crop_year_id: int
    amount: Decimal = Decimal(0)
    farmer_price: Decimal = Decimal(0)
    factory_price: Decimal = Decimal(0)

class FactorySeedSchema(FactorySeedCreate):
    id: int
    created_at: str
    factory_name: str | None
    seed_name: str | None
    unit_name: str | None
    crop_year_name: str | None

class FactorySeedUpdate(PydanticBase):
    factory_id: int
    seed_id: int
    crop_year_id: int
    amount: Decimal = Decimal(0)
    farmer_price: Decimal = Decimal(0)
    factory_price: Decimal = Decimal(0)

class Filters(PydanticBase):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=50 ,ge=1, le=100)
    sort_by: Optional[str] = Field(default="")
    sort_order: Optional[str] = Field(default="")
    factory_id: Optional[int] = Field(default=0)
    seed_id: Optional[int] = Field(default=0)
    crop_year_id: Optional[int] = Field(default=0)

    search: Optional[str] = Field(default="", description="Search in factory name, seed name, or crop year name")