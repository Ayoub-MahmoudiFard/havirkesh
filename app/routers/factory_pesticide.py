from fastapi import APIRouter, HTTPException
from fastapi import APIRouter
from ..database import SessionDep
from ..schemas.factory_pesticide import FactoryPesticideSchema, Filters, FactoryPesticideCreate, FactoryPesticideUpdate
from ..models.factory_pesticide import FactoryPesticides

from ..models.factory import Factories
from ..models.pesticide import Pesticides
from ..models.crop_year import CropYears

from sqlalchemy import select, or_, asc, desc

from fastapi_pagination import Page, paginate

from sqlalchemy.orm import joinedload

# تابع تاریخ شمسی
import jdatetime
def to_jalali(dt):
    if not dt:
        return None
    return jdatetime.datetime.fromgregorian(datetime=dt).strftime('%Y/%m/%d %H:%M')

from fastapi import Depends

router = APIRouter(prefix='/factory_pesticide', tags=["Factory Pesticide"])

@router.post("/")
def create_factory_pesticide(session: SessionDep, factory_pesticide_param: FactoryPesticideCreate):

    factory_pesticide_insert = FactoryPesticides(
        factory_id = factory_pesticide_param.factory_id,
        pesticide_id = factory_pesticide_param.pesticide_id,
        crop_year_id = factory_pesticide_param.crop_year_id,
        amount = factory_pesticide_param.amount,
        farmer_price = factory_pesticide_param.farmer_price,
        factory_price = factory_pesticide_param.factory_price,
    )

    session.add(factory_pesticide_insert)
    session.commit()
    session.refresh(factory_pesticide_insert)

    return {
        "factory_id": factory_pesticide_insert.factory_id,
        "pesticide_id": factory_pesticide_insert.pesticide_id,
        "crop_year_id": factory_pesticide_insert.crop_year_id,
        "amount": factory_pesticide_insert.amount,
        "farmer_price": factory_pesticide_insert.farmer_price,
        "factory_price": factory_pesticide_insert.factory_price,

        "id": factory_pesticide_insert.id,

        # گرفتن فیلد از جدول دیگر
        "crop_year_name": (
            factory_pesticide_insert.crop_year.crop_year_name
            if factory_pesticide_insert.crop_year else None
        ),
        "factory_name": (
            factory_pesticide_insert.factories.factory_name
            if factory_pesticide_insert.factories else None
        ),
        "pesticide_name": (
            factory_pesticide_insert.pesticides.pesticide_name
            if factory_pesticide_insert.pesticides else None
        ),

        # اتصال factory_pesticide → seed → measur_unit
        "unit_name": (
            factory_pesticide_insert.pesticides.measure_unit.unit_name
            if factory_pesticide_insert.pesticides
            and factory_pesticide_insert.pesticides.measure_unit
            else None
        )

    }

@router.get("/")
def select_all_factory_pesticide(session: SessionDep
    , filters: Filters = Depends()) -> Page[FactoryPesticideSchema]:

    # وصل کردن دو جدول به هم
    query = select(FactoryPesticides).options(
        joinedload(FactoryPesticides.crop_year)
    )

    if filters.search:
        search = f"%{filters.search}%"

        query = (
            query
            .join(FactoryPesticides.factories)
            .join(FactoryPesticides.pesticides)
            .where(
                or_(
                    Factories.factory_name.ilike(search),
                    Pesticides.pesticide_name.ilike(search),
                    CropYears.crop_year_name.ilike(search)
                )
            )
        )
    
    if filters.factory_id:
        query = query.where(
            or_(
                FactoryPesticides.factory_id == int(filters.factory_id)
            )
        )
    
    if filters.pesticide_id:
        query = query.where(
            or_(
                FactoryPesticides.pesticide_id == int(filters.pesticide_id)
            )
        )

    if filters.crop_year_id:
        query = query.where(
            or_(
                FactoryPesticides.crop_year_id == int(filters.crop_year_id)
            )
        )

    if filters.sort_by:
        column = getattr(FactoryPesticides, filters.sort_by, None)
        if column is None:
            raise HTTPException(status_code=400, detail="Invalid sort field")

        if filters.sort_order.lower() == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

    factory_pesticide_results = session.execute(query).scalars().all()

    if not factory_pesticide_results:
        raise HTTPException(status_code=404, detail="Record not found")
    
    result = [
        FactoryPesticideSchema(
            factory_id=factory_pesticide_row.factory_id,
            pesticide_id=factory_pesticide_row.pesticide_id,
            crop_year_id=factory_pesticide_row.crop_year_id,
            amount=factory_pesticide_row.amount,
            farmer_price=factory_pesticide_row.farmer_price,
            factory_price=factory_pesticide_row.factory_price,
            id=factory_pesticide_row.id,

            # گرفتن فیلد از جدول دیگر
            factory_name=factory_pesticide_row.factories.factory_name if factory_pesticide_row.factories else None,
            pesticide_name=factory_pesticide_row.pesticides.pesticide_name if factory_pesticide_row.pesticides else None,
            crop_year_name=factory_pesticide_row.crop_year.crop_year_name if factory_pesticide_row.crop_year else None,

            # اتصال factory_pesticide → seed → measur_unit
            unit_name= factory_pesticide_row.pesticides.measure_unit.unit_name if factory_pesticide_row.pesticides and factory_pesticide_row.pesticides.measure_unit else None,

            created_at=to_jalali(factory_pesticide_row.created_at),
        )
        for factory_pesticide_row in factory_pesticide_results
    ]

    return paginate(result)

@router.put('/{id}')
def update_factory_pesticide(session: SessionDep, id: str, factory_pesticide_data: FactoryPesticideUpdate):
    # گرفتن کاربر از دیتابیس
    get_factory_pesticide = session.execute(
        select(FactoryPesticides).where(FactoryPesticides.id == id)
    ).scalars().first()
    
    # جایگزینی تمام فیلدهای کاربر با داده‌های دریافتی
    update_data = factory_pesticide_data.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(get_factory_pesticide, field, value)

    # ذخیره تغییرات در دیتابیس
    session.commit()
    session.refresh(get_factory_pesticide)

    # بازگرداندن اطلاعات کاربر بعد از آپدیت
    return {
        **factory_pesticide_data.__dict__,
        "created_at": to_jalali(get_factory_pesticide.created_at),
    }


@router.delete('/{id}')
def delete_factory_pesticide(session: SessionDep, id: int):
    get_pesticide = session.execute(
        select(FactoryPesticides).where(FactoryPesticides.id == id)
    )

    result = get_pesticide.scalar_one_or_none()

    session.delete(result)
    session.commit()

    return f"product Price {id} delete sucessfuly."