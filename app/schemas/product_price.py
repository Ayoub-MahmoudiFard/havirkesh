from pydantic import BaseModel as PydanticBase
from datetime import datetime

from pydantic import Field
from typing import Optional

class ProductPriceCreate(PydanticBase):
    crop_year_id: int
    sugar_amount_per_ton_kg: str
    sugar_price_per_kg: str
    pulp_amount_per_ton_kg: str
    pulp_price_per_kg: str
    sugar_amount_per_ton_kg: str

class ProductPriceSchema(PydanticBase):
    id: int
    crop_year_id: int
    sugar_amount_per_ton_kg: str
    sugar_price_per_kg: str
    pulp_amount_per_ton_kg: str
    pulp_price_per_kg: str
    sugar_amount_per_ton_kg: str

    crop_year_name: str | None

    created_at: str

class Filters(PydanticBase):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=50 ,ge=1, le=100)
    sort_by: Optional[str] = Field(default="")
    sort_order: Optional[str] = Field(default="")
    crop_year_id: Optional[int] = Field(default=0)