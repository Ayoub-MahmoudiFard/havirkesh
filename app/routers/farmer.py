from fastapi import APIRouter, HTTPException
from fastapi import APIRouter
from ..database import SessionDep
from ..schemas.farmer import FarmerSchema, Filters, FarmerCreate, FarmerUpdate
from ..models.farmer import Farmers

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

from fastapi import Depends

router = APIRouter(prefix='/farmer', tags=["Farmer"])

@router.post("/")
def create_farmer(session: SessionDep, farmer_param: FarmerCreate):

    farmer_insert = Farmers(
        national_id = farmer_param.national_id,
        full_name = farmer_param.full_name,
        father_name = farmer_param.father_name,
        phone_number = farmer_param.phone_number,
        sheba_number_1 = farmer_param.sheba_number_1,
        sheba_number_2 = farmer_param.sheba_number_2,
        card_number = farmer_param.card_number,
        address = farmer_param.address
    )

    session.add(farmer_insert)
    session.commit()
    session.refresh(farmer_insert)

    return {
        "id": farmer_insert.id,
        "national_id": farmer_insert.national_id,
        "full_name": farmer_insert.full_name,
        "father_name": farmer_insert.father_name,
        "phone_number": farmer_insert.phone_number,
        "sheba_number_1": farmer_insert.sheba_number_1,
        "sheba_number_2": farmer_insert.sheba_number_2,
        "card_number": farmer_insert.card_number,
        "address": farmer_insert.address,
        "created_at": to_jalali(farmer_insert.created_at)
    }

@router.get("/")
def select_all_farmer(session: SessionDep
    , filters: Filters = Depends()) -> Page[FarmerSchema]:

    query = select(Farmers)
    
    if filters.search:

        search = f"%{filters.search}%"

        query = query.where(
            or_(
                Farmers.full_name.ilike(search),
                Farmers.national_id.ilike(search),
                Farmers.father_name.ilike(search),
                Farmers.address.ilike(search),
                Farmers.phone_number.ilike(search),
            )
        )

    if filters.sort_by:
        column = getattr(Farmers, filters.sort_by, None)
        if column is None:
            raise HTTPException(status_code=400, detail="Invalid sort field")

        if filters.sort_order.lower() == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

    farmer_results = session.execute(query).scalars().all()

    if not farmer_results:
        raise HTTPException(status_code=404, detail="Record not found")
    
    result = [
        FarmerSchema(
            id=farmer_row.id,
            full_name=farmer_row.full_name,

            national_id=farmer_row.national_id,
            father_name=farmer_row.father_name,
            phone_number=farmer_row.phone_number,
            sheba_number_1=farmer_row.sheba_number_1,
            sheba_number_2=farmer_row.sheba_number_2,
            card_number=farmer_row.card_number,
            address=farmer_row.address,

            created_at= to_jalali(farmer_row.created_at),
        )
        for farmer_row in farmer_results
    ]

    return paginate(result)

@router.get('/{national_id}', response_model=FarmerSchema)
def get_farmer_by_national_id(session: SessionDep, national_id: str):
    get_farmer = session.execute(
        select(Farmers).where(Farmers.national_id == national_id)
    )
    
    get_farmer = get_farmer.scalars().first()

    if not get_farmer:
        raise HTTPException(status_code=404, detail="Record not found")

    return {
        **get_farmer.__dict__,
        "created_at": to_jalali(get_farmer.created_at),
    }

@router.put('/{national_id}')
def update_farmer(session: SessionDep, national_id: str, farmer_data: FarmerUpdate):
    # گرفتن کاربر از دیتابیس
    get_farmer = session.execute(
        select(Farmers).where(Farmers.national_id == national_id)
    ).scalars().first()
    
    # جایگزینی تمام فیلدهای کاربر با داده‌های دریافتی
    update_data = farmer_data.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(get_farmer, field, value)

    # ذخیره تغییرات در دیتابیس
    session.commit()
    session.refresh(get_farmer)

    # بازگرداندن اطلاعات کاربر بعد از آپدیت
    return {
        **farmer_data.__dict__,
        "created_at": to_jalali(get_farmer.created_at),
    }


@router.delete('/{national_id}')
def delete_farmer(session: SessionDep, national_id: str):
    get_farmer = session.execute(
        select(Farmers).where(Farmers.national_id == national_id)
    )

    result = get_farmer.scalar_one_or_none()

    session.delete(result)
    session.commit()

    return {
        "message": "Farmer Deleted."
    }