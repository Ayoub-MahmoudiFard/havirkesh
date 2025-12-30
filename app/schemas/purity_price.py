from pydantic import BaseModel as PydanticBase
from datetime import datetime

from pydantic import Field
from typing import Optional

from decimal import Decimal

class PurityPriceCreate(PydanticBase):
    crop_year_id: int
    base_purity: int
    base_purity_price: Decimal = Decimal(0)
    price_difference: Decimal = Decimal(0)

class PurityPriceSchema(PydanticBase):
    id: int
    crop_year_id: int
    base_purity: int
    base_purity_price: Decimal = Decimal(0)
    price_difference: Decimal = Decimal(0)

    crop_year_name: str | None

    created_at: str

class Filters(PydanticBase):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=50 ,ge=1, le=100)
    sort_by: Optional[str] = Field(default="")
    sort_order: Optional[str] = Field(default="")
    crop_year_id: Optional[int] = Field(default=0)