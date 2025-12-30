from fastapi import APIRouter, HTTPException
from fastapi import APIRouter
from ..database import SessionDep
from ..schemas.measure_unit import MeasurUnitSchema, Filters, MeasurUnitCreate
from ..models.measure_unit import MeasurUnites

from sqlalchemy import select, or_, asc, desc

from fastapi_pagination import Page, paginate

# تابع تاریخ شمسی
import jdatetime
def to_jalali(dt):
    if not dt:
        return None
    return jdatetime.datetime.fromgregorian(datetime=dt).strftime('%Y/%m/%d %H:%M')

from fastapi import Depends

router = APIRouter(prefix='/measur_unite', tags=["Measur Unites"])

@router.post("/")
def create_measur_unite(session: SessionDep, measur_unit_param: MeasurUnitCreate):

    measur_unite_insert = MeasurUnites(
        unit_name = measur_unit_param.unit_name
    )

    session.add(measur_unite_insert)
    session.commit()
    session.refresh(measur_unite_insert)

    return {
        "unit_name": measur_unite_insert.unit_name,
        "id": measur_unite_insert.id,
        "created_at": to_jalali(measur_unite_insert.created_at)
    }

@router.get("/")
def select_all_measure_unite(session: SessionDep
    , filters: Filters = Depends()) -> Page[MeasurUnitSchema]:

    query = select(MeasurUnites)
    
    if filters.search:
        query = query.where(
            or_(
                MeasurUnites.unit_name.ilike(f"%{filters.search}%"),
            )
        )

    if filters.sort_by:
        column = getattr(MeasurUnites, filters.sort_by, None)
        if column is None:
            raise HTTPException(status_code=400, detail="Invalid sort field")

        if filters.sort_order.lower() == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

    measur_unite_results = session.execute(query).scalars().all()

    if not measur_unite_results:
        raise HTTPException(status_code=404, detail="Record not found")
    
    result = [
        MeasurUnitSchema(
            id=measur_unite_row.id,
            unit_name=measur_unite_row.unit_name,
            created_at= to_jalali(measur_unite_row.created_at),
        )
        for measur_unite_row in measur_unite_results
    ]

    return paginate(result)

@router.delete('/{unit_name}')
def delete_unit_name(session: SessionDep, unit_name: str):
    get_unit_name = session.execute(
        select(MeasurUnites).where(MeasurUnites.unit_name == unit_name)
    )

    result = get_unit_name.scalar_one_or_none()

    session.delete(result)
    session.commit()

    return f"unit name {unit_name} delete sucessfuly."