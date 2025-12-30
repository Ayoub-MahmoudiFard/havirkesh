from fastapi import APIRouter, HTTPException
from fastapi import APIRouter
from ..database import SessionDep
from ..schemas.provinces import ProvincesSchema, Filters, ProvincesCreate
from ..models.provinces import Provinces

from sqlalchemy import select, or_, asc, desc

from fastapi_pagination import Page, paginate

# تابع تاریخ شمسی
import jdatetime
def to_jalali(dt):
    if not dt:
        return None
    return jdatetime.datetime.fromgregorian(datetime=dt).strftime('%Y/%m/%d %H:%M')

from fastapi import Depends

router = APIRouter(prefix='/province', tags=["Province"])

@router.post("/", response_model=ProvincesCreate)
def create_province(session: SessionDep, province_param: ProvincesCreate):

    province_insert = Provinces(
        province=province_param.province
    )

    session.add(province_insert)
    session.commit()
    session.refresh(province_insert)

    return {
        "status": "success",
        "province": province_insert.province
    }


@router.get('/')
def select_all_provinces(session: SessionDep
    , filters: Filters = Depends()) -> Page[ProvincesSchema]:

    query = select(Provinces)
    
    if filters.search:
        query = query.where(
            or_(
                Provinces.province.ilike(f"%{filters.search}%"),
            )
        )

    if filters.sort_by:
        column = getattr(Provinces, filters.sort_by, None)
        if column is None:
            raise HTTPException(status_code=400, detail="Invalid sort field")

        if filters.sort_order.lower() == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

    province_results = session.execute(query).scalars().all()

    if not province_results:
        raise HTTPException(status_code=404, detail="Record not found")
    
    result = [
        ProvincesSchema(
            id=province_row.id,
            province=province_row.province,
            created_at=to_jalali(province_row.created_at),
        )
        for province_row in province_results
    ]

    return paginate(result)

@router.delete('/{province}')
def delete_province(session: SessionDep, province: int):
    get_province = session.execute(
        select(Provinces).where(Provinces.id == province)
    )

    result = get_province.scalar_one_or_none()

    session.delete(result)
    session.commit()

    return f"Province {province} delete sucessfuly."