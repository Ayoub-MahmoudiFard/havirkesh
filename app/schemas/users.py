# Path: برای اعتبار سنجی های مربوط به Path paramete ها
# Query: برای اعتبار سنجی های مربوط به Query paramete ها
from fastapi import Path, Query
from pydantic import BaseModel as PydanticBase

# برای تعریف نوع داده تاریخ
from datetime import datetime

# جهت ایجاد فیلد برای کوئری استرینگ فیلترهای جستجو
from pydantic import Field

from typing import Optional

class UsersCreate(PydanticBase):
    username: str
    password: str
    fullname: str
    email: str
    disabled: bool = Path(description="Default=false")
    role_id: int
    phone_number: str

class UserGet(PydanticBase):
    created_at: datetime
    created_at_jalali: Optional[str]
    updated_at: datetime
    updated_at_jalali: Optional[str]
    id: int
    username: str
    email: str
    fullname: str
    phone_number: str
    role_id: int
    disabled: bool = Path(description="Default=false")

class UserUpdate(PydanticBase):
    username: Optional[str] = None
    password: Optional[str] = None
    fullname: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    role_id: Optional[int] = None
    disabled: Optional[bool] = None

class Filters(PydanticBase):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=50 ,ge=1, le=100)
    sort_by: Optional[str] = Field(default="")
    sort_order: Optional[str] = Field(default="")
    search: Optional[str] = Field(default="")