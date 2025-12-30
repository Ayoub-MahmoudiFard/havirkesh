from fastapi import APIRouter, HTTPException
from fastapi import APIRouter
from ..database import SessionDep
from ..schemas.crop_year import CropYearSchema, Filters, CropYearCreate
from ..models.crop_year import CropYears

from sqlalchemy import select, or_, asc, desc

from fastapi_pagination import Page, paginate

# تابع تاریخ شمسی
import jdatetime
def to_jalali(dt):
    if not dt:
        return None
    return jdatetime.datetime.fromgregorian(datetime=dt).strftime('%Y/%m/%d %H:%M')

from fastapi import Depends

router = APIRouter(prefix='/crop_year', tags=["Crop Year"])

@router.post("/")
def create_crop_year(session: SessionDep, crop_year_param: CropYearCreate):

    crop_year_insert = CropYears(
        crop_year_name = crop_year_param.crop_year_name
    )

    session.add(crop_year_insert)
    session.commit()
    session.refresh(crop_year_insert)

    return {
        "crop_year_name": crop_year_insert.crop_year_name,
        "id": crop_year_insert.id,
        "created_at": to_jalali(crop_year_insert.created_at)
    }

@router.get("/")
def select_all_crop_year(session: SessionDep
    , filters: Filters = Depends()) -> Page[CropYearSchema]:

    query = select(CropYears)
    
    if filters.search:
        query = query.where(
            or_(
                CropYears.crop_year_name.ilike(f"%{filters.search}%"),
            )
        )

    if filters.sort_by:
        column = getattr(CropYears, filters.sort_by, None)
        if column is None:
            raise HTTPException(status_code=400, detail="Invalid sort field")

        if filters.sort_order.lower() == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

    crop_year_results = session.execute(query).scalars().all()

    if not crop_year_results:
        raise HTTPException(status_code=404, detail="Record not found")
    
    result = [
        CropYearSchema(
            id=crop_year_row.id,
            crop_year_name=crop_year_row.crop_year_name,
            created_at= to_jalali(crop_year_row.created_at),
        )
        for crop_year_row in crop_year_results
    ]

    return paginate(result)

@router.delete('/{crop_year_name}')
def delete_crop_year_name(session: SessionDep, crop_year_name: str):
    get_crop_year_name = session.execute(
        select(CropYears).where(CropYears.crop_year_name == crop_year_name)
    )

    result = get_crop_year_name.scalar_one_or_none()

    session.delete(result)
    session.commit()

    return f"crop year {crop_year_name} delete sucessfuly."