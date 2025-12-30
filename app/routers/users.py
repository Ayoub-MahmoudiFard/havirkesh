from fastapi import APIRouter, HTTPException, Query
# DabaBase
from ..database import SessionDep
# Schemas
from ..schemas.users import UsersCreate, UserUpdate, Filters, UserGet
# model
from ..models.users import Users

from sqlalchemy import select, or_, asc, desc

from fastapi_pagination import Page, paginate

# تابع هش کردن
from passlib.hash import sha256_crypt
def hash_password(password: str) -> str:
    return sha256_crypt.hash(password)

# تابع تاریخ شمسی
import jdatetime
def to_jalali(dt):
    if not dt:
        return None
    return jdatetime.datetime.fromgregorian(datetime=dt).strftime('%Y/%m/%d %H:%M')

# جهت تزریق وابستگی فیلد به روتر در فیلترهای جستجو -> select_all_user
from fastapi import Depends

# Create rout
router = APIRouter(prefix='/users', tags=["Users"])

# برگرداندن فیلدهای تعیین شده برای خروجی بعد از ثبت
@router.post("/admin/")
def create_user(session: SessionDep, user: UsersCreate):
    user_insert = Users(
        username=user.username,
        password=user.password,
        fullname=user.fullname,
        email=user.email,
        disabled=user.disabled,
        role_id=user.role_id,
        phone_number=user.phone_number
    )

    session.add(user_insert)
    session.commit()
    session.refresh(user_insert)

    return {
        "status": "success",
        "username": user_insert.username
    }

@router.get('/{user_id}', response_model=UserGet)
def select_user(session: SessionDep, user_id: int):
    get_user = session.execute(
        select(Users).where(Users.id == user_id)
    )
    
    get_user = get_user.scalars().first()

    if not get_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        **get_user.__dict__,
        "created_at_jalali": to_jalali(get_user.created_at),
        "updated_at_jalali": to_jalali(get_user.updated_at),
    }

@router.put('/{user_id}')
def update_user(session: SessionDep, user_id: int, user_data: UserUpdate):
    # گرفتن کاربر از دیتابیس
    get_user = session.get(Users, user_id)

    if not get_user:
        raise HTTPException(status_code=404, detail="User {user_id} not found")
    
    # جایگزینی تمام فیلدهای کاربر با داده‌های دریافتی
    update_data = user_data.dict(exclude_unset=True)

    # هش کردن پسورد در صورت وجود
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    for field, value in update_data.items():
        setattr(get_user, field, value)

    # ذخیره تغییرات در دیتابیس
    session.commit()
    session.refresh(get_user)

    # بازگرداندن اطلاعات کاربر بعد از آپدیت
    return {
        **user_data.__dict__,
        "created_at_jalali": to_jalali(get_user.created_at),
        "updated_at_jalali": to_jalali(get_user.updated_at),
    }

@router.get('/')
def select_all_user(session: SessionDep
    , filters: Filters = Depends()) -> Page[UserGet]:

    query = select(Users)
    
    if filters.search:
        query = query.where(
            or_(
                Users.username.ilike(f"%{filters.search}%"),
                Users.email.ilike(f"%{filters.search}%")
            )
        )

    if filters.sort_by:
        column = getattr(Users, filters.sort_by, None)
        if column is None:
            raise HTTPException(status_code=400, detail="Invalid sort field")

        if filters.sort_order.lower() == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

    user_results = session.execute(query).scalars().all()

    if not user_results:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 🔁 تبدیل رکوردها قبل از paginate
    result = [
        UserGet(
            **user.__dict__,
            created_at_jalali=to_jalali(user.created_at),
            updated_at_jalali=to_jalali(user.updated_at),
        )
        for user in user_results
    ]

    return paginate(result)