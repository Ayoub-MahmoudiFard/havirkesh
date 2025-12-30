from pydantic import BaseModel as PydanticBase
from datetime import datetime

from pydantic import Field
from typing import Optional

class SeedCreate(PydanticBase):
    seed_name: str
    measure_unit_id: int

class SeedSchema(PydanticBase):
    id: int
    seed_name: str
    measure_unit_id: int

    measure_unit_name: str | None

    created_at: str

class Filters(PydanticBase):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=50 ,ge=1, le=100)
    sort_by: Optional[str] = Field(default="")
    sort_order: Optional[str] = Field(default="")
    search: Optional[str] = Field(default="")