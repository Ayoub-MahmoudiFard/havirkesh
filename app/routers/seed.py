from fastapi import APIRouter, HTTPException
from fastapi import APIRouter
from ..database import SessionDep
from ..schemas.seed import SeedSchema, Filters, SeedCreate
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

router = APIRouter(prefix='/seed', tags=["Seed"])

@router.post("/")
def create_seed(session: SessionDep, seed_param: SeedCreate):

    seed_insert = Seeds(
        seed_name = seed_param.seed_name,
        measure_unit_id = seed_param.measure_unit_id
    )

    session.add(seed_insert)
    session.commit()
    session.refresh(seed_insert)

    return {
        "id": seed_insert.id,
        "seed_name": seed_insert.seed_name,
        "measure_unit_id": seed_insert.measure_unit_id,
        # گرفتن فیلد از جدول دیگر
        "measure_unit_name": (
            seed_insert.measure_unit.unit_name
            if seed_insert.measure_unit else None
        )
    }

@router.get("/")
def select_all_seed(session: SessionDep
    , filters: Filters = Depends()) -> Page[SeedSchema]:

    # وصل کردن دو جدول به هم
    query = select(Seeds).options(
        joinedload(Seeds.measure_unit)
    )
    
    if filters.search:
        query = query.where(
            or_(
                Seeds.seed_name.ilike(f"%{filters.search}%"),
            )
        )

    if filters.sort_by:
        column = getattr(Seeds, filters.sort_by, None)
        if column is None:
            raise HTTPException(status_code=400, detail="Invalid sort field")

        if filters.sort_order.lower() == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

    seed_results = session.execute(query).scalars().all()

    if not seed_results:
        raise HTTPException(status_code=404, detail="Record not found")
    
    result = [
        SeedSchema(
            id=seed_row.id,
            measure_unit_id=seed_row.measure_unit_id,
            seed_name=seed_row.seed_name,

            # گرفتن فیلد از جدول دیگر
            measure_unit_name=seed_row.measure_unit.unit_name if seed_row.measure_unit else None,

            created_at=to_jalali(seed_row.created_at),
        )
        for seed_row in seed_results
    ]

    return paginate(result)

@router.delete('/{seed}')
def delete_seed(session: SessionDep, seed: str):
    get_pesticide = session.execute(
        select(Seeds).where(Seeds.seed_name == seed)
    )

    result = get_pesticide.scalar_one_or_none()

    session.delete(result)
    session.commit()

    return f"seed {seed} delete sucessfuly."