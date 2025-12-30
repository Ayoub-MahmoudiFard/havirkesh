from pydantic import BaseModel as PydanticBase
from datetime import datetime

from pydantic import Field
from typing import Optional

from decimal import Decimal

from fastapi import Query

class FactoryPesticideCreate(PydanticBase):
    factory_id: int
    pesticide_id: int
    crop_year_id: int
    amount: Decimal = Decimal(0)
    farmer_price: Decimal = Decimal(0)
    factory_price: Decimal = Decimal(0)

class FactoryPesticideSchema(FactoryPesticideCreate):
    id: int
    created_at: str
    factory_name: str | None
    pesticide_name: str | None
    unit_name: str | None
    crop_year_name: str | None

class FactoryPesticideUpdate(PydanticBase):
    factory_id: int
    pesticide_id: int
    crop_year_id: int
    amount: Decimal = Decimal(0)
    farmer_price: Decimal = Decimal(0)
    factory_price: Decimal = Decimal(0)

class Filters(PydanticBase):
    page: int = Query(default=1, ge=1)
    size: int = Query(default=50 ,ge=1, le=100)
    sort_by: Optional[str] = Query(None)
    sort_order: Optional[str] = Query(None)
    factory_id: Optional[int] = Query(None)
    pesticide_id: Optional[int] = Query(None)
    crop_year_id: Optional[int] = Query(None)

    search: Optional[str] = Query(None, description="Search in factory name, seed name, or crop year name")