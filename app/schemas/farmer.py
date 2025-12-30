from pydantic import BaseModel as PydanticBase
from datetime import datetime

from pydantic import Field
from typing import Optional

class FarmerCreate(PydanticBase):
    national_id: str
    full_name: str
    father_name: str
    phone_number: str
    sheba_number_1: str
    sheba_number_2: str
    card_number: str
    address: str

class FarmerSchema(PydanticBase):
    national_id: str
    full_name: str
    father_name: str
    phone_number: str
    sheba_number_1: str
    sheba_number_2: str
    card_number: str
    address: str
    id: int
    created_at: str

class FarmerUpdate(PydanticBase):
    full_name: str
    father_name: str
    phone_number: str
    sheba_number_1: str
    sheba_number_2: str
    card_number: str
    address: str

class Filters(PydanticBase):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=50 ,ge=1, le=100)
    sort_by: Optional[str] = Field(default="")
    sort_order: Optional[str] = Field(default="")
    search: Optional[str] = Field(default="", description="Search term for full name, national ID, father name, address, or phone number")