from fastapi import APIRouter, HTTPException
from fastapi import APIRouter
from ..database import SessionDep
from ..schemas.factory_seed import FactorySeedSchema, Filters, FactorySeedCreate, FactorySeedUpdate
from ..models.factory_seed import FactorySeeds

from ..models.factory import Factories
from ..models.seed import Seeds


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

router = APIRouter(prefix='/factory_seed', tags=["Factory Seed"])

@router.post("/")
def create_factory_seed(session: SessionDep, factory_seed_param: FactorySeedCreate):

    factory_seed_insert = FactorySeeds(
        factory_id = factory_seed_param.factory_id,
        seed_id = factory_seed_param.seed_id,
        crop_year_id = factory_seed_param.crop_year_id,
        amount = factory_seed_param.amount,
        farmer_price = factory_seed_param.farmer_price,
        factory_price = factory_seed_param.factory_price,
    )

    session.add(factory_seed_insert)
    session.commit()
    session.refresh(factory_seed_insert)

    return {
        "factory_id": factory_seed_insert.factory_id,
        "seed_id": factory_seed_insert.seed_id,
        "crop_year_id": factory_seed_insert.crop_year_id,
        "amount": factory_seed_insert.amount,
        "farmer_price": factory_seed_insert.farmer_price,
        "factory_price": factory_seed_insert.factory_price,

        "id": factory_seed_insert.id,

        # گرفتن فیلد از جدول دیگر
        "crop_year_name": (
            factory_seed_insert.crop_year.crop_year_name
            if factory_seed_insert.crop_year else None
        ),
        "factory_name": (
            factory_seed_insert.factories.factory_name
            if factory_seed_insert.factories else None
        ),
        "seed_name": (
            factory_seed_insert.seeds.seed_name
            if factory_seed_insert.seeds else None
        ),

        # اتصال factory_seed → seed → measur_unit
        "unit_name": (
            factory_seed_insert.seeds.measure_unit.unit_name
            if factory_seed_insert.seeds
            and factory_seed_insert.seeds.measure_unit
            else None
        )

    }

@router.get("/")
def select_all_factory_seed(session: SessionDep
    , filters: Filters = Depends()) -> Page[FactorySeedSchema]:

    # وصل کردن دو جدول به هم
    query = select(FactorySeeds).options(
        joinedload(FactorySeeds.crop_year)
    )

    if filters.search:
        search = f"%{filters.search}%"

        query = (
            query
            .join(FactorySeeds.factories)
            .join(FactorySeeds.seeds)
            .where(
                or_(
                    Factories.factory_name.ilike(search),
                    Seeds.seed_name.ilike(search),
                )
            )
        )
    
    if filters.factory_id:
        query = query.where(
            or_(
                FactorySeeds.factory_id == int(filters.factory_id)
            )
        )
    
    if filters.seed_id:
        query = query.where(
            or_(
                FactorySeeds.seed_id == int(filters.seed_id)
            )
        )

    if filters.crop_year_id:
        query = query.where(
            or_(
                FactorySeeds.crop_year_id == int(filters.crop_year_id)
            )
        )

    if filters.sort_by:
        column = getattr(FactorySeeds, filters.sort_by, None)
        if column is None:
            raise HTTPException(status_code=400, detail="Invalid sort field")

        if filters.sort_order.lower() == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

    factory_seeds_results = session.execute(query).scalars().all()

    if not factory_seeds_results:
        raise HTTPException(status_code=404, detail="REcord not found")
    
    result = [
        FactorySeedSchema(
            factory_id=factory_seeds_row.factory_id,
            seed_id=factory_seeds_row.seed_id,
            crop_year_id=factory_seeds_row.crop_year_id,
            amount=factory_seeds_row.amount,
            farmer_price=factory_seeds_row.farmer_price,
            factory_price=factory_seeds_row.factory_price,
            id=factory_seeds_row.id,

            # گرفتن فیلد از جدول دیگر
            factory_name=factory_seeds_row.factories.factory_name if factory_seeds_row.factories else None,
            seed_name=factory_seeds_row.seeds.seed_name if factory_seeds_row.seeds else None,
            crop_year_name=factory_seeds_row.crop_year.crop_year_name if factory_seeds_row.crop_year else None,

            # اتصال factory_seed → seed → measur_unit
            unit_name= factory_seeds_row.seeds.measure_unit.unit_name if factory_seeds_row.seeds and factory_seeds_row.seeds.measure_unit else None,

            created_at=to_jalali(factory_seeds_row.created_at),
        )
        for factory_seeds_row in factory_seeds_results
    ]

    return paginate(result)

@router.put('/{id}')
def update_factory_seed(session: SessionDep, id: str, factory_seed_data: FactorySeedUpdate):
    # گرفتن کاربر از دیتابیس
    get_factory_seed = session.execute(
        select(FactorySeeds).where(FactorySeeds.id == id)
    ).scalars().first()
    
    # جایگزینی تمام فیلدهای کاربر با داده‌های دریافتی
    update_data = factory_seed_data.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(get_factory_seed, field, value)

    # ذخیره تغییرات در دیتابیس
    session.commit()
    session.refresh(get_factory_seed)

    # بازگرداندن اطلاعات کاربر بعد از آپدیت
    return {
        **factory_seed_data.__dict__,
        "created_at": to_jalali(get_factory_seed.created_at),
    }


@router.delete('/{id}')
def delete_factory_seed(session: SessionDep, id: int):
    get_pesticide = session.execute(
        select(FactorySeeds).where(FactorySeeds.id == id)
    )

    result = get_pesticide.scalar_one_or_none()

    session.delete(result)
    session.commit()

    return f"product Price {id} delete sucessfuly."