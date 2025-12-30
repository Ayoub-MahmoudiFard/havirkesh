from fastapi import APIRouter, HTTPException
from fastapi import APIRouter
from ..database import SessionDep
from ..schemas.village import VillageSchema, Filters, VillageCreate
from ..models.village import Villages

from sqlalchemy import select, or_, asc, desc

from fastapi_pagination import Page, paginate

# تابع تاریخ شمسی
import jdatetime
def to_jalali(dt):
    if not dt:
        return None
    return jdatetime.datetime.fromgregorian(datetime=dt).strftime('%Y/%m/%d %H:%M')

from fastapi import Depends

router = APIRouter(prefix='/village', tags=["Village"])

@router.post("/")
def create_village(session: SessionDep, village_param: VillageCreate):

    village_insert = Villages(
        village = village_param.village,
        city_id = village_param.city_id
    )

    session.add(village_insert)
    session.commit()
    session.refresh(village_insert)

    return {
        "status": "success",
        "village": village_insert.village
    }

@router.get("/")
def select_all_villages(session: SessionDep
    , filters: Filters = Depends()) -> Page[VillageSchema]:

    query = select(Villages)
    
    if filters.search:
        query = query.where(
            or_(
                Villages.village.ilike(f"%{filters.search}%"),
            )
        )

    if filters.sort_by:
        column = getattr(Villages, filters.sort_by, None)
        if column is None:
            raise HTTPException(status_code=400, detail="Invalid sort field")

        if filters.sort_order.lower() == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

    village_results = session.execute(query).scalars().all()

    if not village_results:
        raise HTTPException(status_code=404, detail="Record not found")
    
    result = [
        VillageSchema(
            id=village_row.id,
            city_id=village_row.city_id,
            village=village_row.village,
            created_at=to_jalali(village_row.created_at),
        )
        for village_row in village_results
    ]

    return paginate(result)

@router.delete('/{village}')
def delete_village(session: SessionDep, village: int):
    get_village = session.execute(
        select(Villages).where(Villages.id == village)
    )

    result = get_village.scalar_one_or_none()

    session.delete(result)
    session.commit()

    return f"village {village} delete sucessfuly."