from fastapi import APIRouter, HTTPException
from fastapi import APIRouter
from ..database import SessionDep
from ..schemas.factory import FactorySchema, Filters, FactoryCreate
from ..models.factory import Factories

from sqlalchemy import select, or_, asc, desc

from fastapi_pagination import Page, paginate

# تابع تاریخ شمسی
import jdatetime
def to_jalali(dt):
    if not dt:
        return None
    return jdatetime.datetime.fromgregorian(datetime=dt).strftime('%Y/%m/%d %H:%M')

from fastapi import Depends

router = APIRouter(prefix='/factory', tags=["Factory"])

@router.post("/")
def create_factory(session: SessionDep, factory_param: FactoryCreate):

    factory_insert = Factories(
        factory_name = factory_param.factory_name
    )

    session.add(factory_insert)
    session.commit()
    session.refresh(factory_insert)

    return {
        "status": "success",
        "factory": factory_insert.factory_name
    }

@router.get("/")
def select_all_factores(session: SessionDep
    , filters: Filters = Depends()) -> Page[FactorySchema]:

    query = select(Factories)
    
    if filters.search:
        query = query.where(
            or_(
                Factories.factory_name.ilike(f"%{filters.search}%"),
            )
        )

    if filters.sort_by:
        column = getattr(Factories, filters.sort_by, None)
        if column is None:
            raise HTTPException(status_code=400, detail="Invalid sort field")

        if filters.sort_order.lower() == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

    factory_results = session.execute(query).scalars().all()

    if not factory_results:
        raise HTTPException(status_code=404, detail="Record not found")
    
    result = [
        FactorySchema(
            id=factory_row.id,
            factory_name=factory_row.factory_name,
            created_at=to_jalali(factory_row.created_at),
        )
        for factory_row in factory_results
    ]

    return paginate(result)

@router.delete('/{factory}')
def delete_factory(session: SessionDep, factory: int):
    get_factory = session.execute(
        select(Factories).where(Factories.id == factory)
    )

    result = get_factory.scalar_one_or_none()

    session.delete(result)
    session.commit()

    return f"factory {factory} delete sucessfuly."