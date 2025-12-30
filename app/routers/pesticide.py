from fastapi import APIRouter, HTTPException
from fastapi import APIRouter
from ..database import SessionDep
from ..schemas.pesticide import PesticideSchema, Filters, PesticideCreate
from ..models.pesticide import Pesticides

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

router = APIRouter(prefix='/pesticide', tags=["Pesticide"])

@router.post("/")
def create_pesticide(session: SessionDep, pesticide_param: PesticideCreate):

    pesticide_insert = Pesticides(
        pesticide_name = pesticide_param.pesticide_name,
        measure_unit_id = pesticide_param.measure_unit_id
    )

    session.add(pesticide_insert)
    session.commit()
    session.refresh(pesticide_insert)

    return {
        "id": pesticide_insert.id,
        "pesticide_name": pesticide_insert.pesticide_name,
        "measure_unit_id": pesticide_insert.measure_unit_id,
        # گرفتن فیلد از جدول دیگر
        "unit_name": (
            pesticide_insert.measure_unit.unit_name
            if pesticide_insert.measure_unit else None
        )
    }

@router.get("/")
def select_all_pesticide(session: SessionDep
    , filters: Filters = Depends()) -> Page[PesticideSchema]:

    # وصل کردن دو جدول به هم
    query = select(Pesticides).options(
        joinedload(Pesticides.measure_unit)
    )
    
    if filters.search:
        query = query.where(
            or_(
                Pesticides.pesticide_name.ilike(f"%{filters.search}%"),
            )
        )

    if filters.sort_by:
        column = getattr(Pesticides, filters.sort_by, None)
        if column is None:
            raise HTTPException(status_code=400, detail="Invalid sort field")

        if filters.sort_order.lower() == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

    pesticide_results = session.execute(query).scalars().all()

    if not pesticide_results:
        raise HTTPException(status_code=404, detail="Record not found")
    
    result = [
        PesticideSchema(
            id=pesticide_row.id,
            measure_unit_id=pesticide_row.measure_unit_id,
            pesticide_name=pesticide_row.pesticide_name,

            # گرفتن فیلد از جدول دیگر
            measure_unit_name=pesticide_row.measure_unit.unit_name if pesticide_row.measure_unit else None,

            created_at=to_jalali(pesticide_row.created_at),
        )
        for pesticide_row in pesticide_results
    ]

    return paginate(result)

@router.delete('/{pesticide}')
def delete_pesticide(session: SessionDep, pesticide: str):
    get_pesticide = session.execute(
        select(Pesticides).where(Pesticides.pesticide_name == pesticide)
    )

    result = get_pesticide.scalar_one_or_none()

    session.delete(result)
    session.commit()

    return f"pesticide {pesticide} delete sucessfuly."