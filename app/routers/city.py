from fastapi import APIRouter, HTTPException
from fastapi import APIRouter
from ..database import SessionDep
from ..schemas.city import CitySchema, Filters, CityCreate
from ..models.city import Cities

from sqlalchemy import select, or_, asc, desc

from fastapi_pagination import Page, paginate

# تابع تاریخ شمسی
import jdatetime
def to_jalali(dt):
    if not dt:
        return None
    return jdatetime.datetime.fromgregorian(datetime=dt).strftime('%Y/%m/%d %H:%M')

from fastapi import Depends

router = APIRouter(prefix='/city', tags=["City"])

@router.post("/")
def create_city(session: SessionDep, city_param: CityCreate):

    city_insert = Cities(
        city = city_param.city,
        province_id = city_param.province_id
    )

    session.add(city_insert)
    session.commit()
    session.refresh(city_insert)

    return {
        "status": "success",
        "city": city_insert.city
    }

@router.get("/")
def select_all_cities(session: SessionDep
    , filters: Filters = Depends()) -> Page[CitySchema]:

    query = select(Cities)
    
    if filters.search:
        query = query.where(
            or_(
                Cities.city.ilike(f"%{filters.search}%"),
            )
        )

    if filters.sort_by:
        column = getattr(Cities, filters.sort_by, None)
        if column is None:
            raise HTTPException(status_code=400, detail="Invalid sort field")

        if filters.sort_order.lower() == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

    city_results = session.execute(query).scalars().all()

    if not city_results:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = [
        CitySchema(
            id=city_row.id,
            province_id=city_row.province_id,
            city=city_row.city,
            created_at=to_jalali(city_row.created_at),
        )
        for city_row in city_results
    ]

    return paginate(result)

@router.delete('/{city}')
def delete_city(session: SessionDep, city: int):
    get_city = session.execute(
        select(Cities).where(Cities.id == city)
    )

    result = get_city.scalar_one_or_none()

    session.delete(result)
    session.commit()

    return f"city {city} delete sucessfuly."