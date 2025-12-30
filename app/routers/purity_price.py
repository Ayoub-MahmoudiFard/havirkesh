from fastapi import APIRouter, HTTPException
from fastapi import APIRouter
from ..database import SessionDep
from ..schemas.purity_price import PurityPriceSchema, Filters, PurityPriceCreate
from ..models.purity_price import PurityPrices

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

router = APIRouter(prefix='/purity_price', tags=["Purity Price"])

@router.post("/")
def create_purity_price(session: SessionDep, purity_price_param: PurityPriceCreate):

    purity_price_insert = PurityPrices(
        crop_year_id = purity_price_param.crop_year_id,
        base_purity = purity_price_param.base_purity,
        base_purity_price = purity_price_param.base_purity_price,
        price_difference = purity_price_param.price_difference,
    )

    session.add(purity_price_insert)
    session.commit()
    session.refresh(purity_price_insert)

    return {
        "id": purity_price_insert.id,
        "crop_year_id": purity_price_insert.crop_year_id,
        "base_purity": purity_price_insert.base_purity,
        "base_purity_price": purity_price_insert.base_purity_price,
        "price_difference": purity_price_insert.price_difference,
        # گرفتن فیلد از جدول دیگر
        "crop_year_name": (
            purity_price_insert.crop_year.crop_year_name
            if purity_price_insert.crop_year else None
        )
    }

@router.get("/")
def select_all_purity_price(session: SessionDep
    , filters: Filters = Depends()) -> Page[PurityPriceSchema]:

    # وصل کردن دو جدول به هم
    query = select(PurityPrices).options(
        joinedload(PurityPrices.crop_year)
    )
    
    if filters.crop_year_id:
        query = query.where(
            or_(
                PurityPrices.crop_year_id == int(filters.crop_year_id)
            )
        )

    if filters.sort_by:
        column = getattr(PurityPrices, filters.sort_by, None)
        if column is None:
            raise HTTPException(status_code=400, detail="Invalid sort field")

        if filters.sort_order.lower() == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

    purity_prices_results = session.execute(query).scalars().all()

    if not purity_prices_results:
        raise HTTPException(status_code=404, detail="Record not found")
    
    result = [
        PurityPriceSchema(
            id=purity_prices_row.id,
            crop_year_id=purity_prices_row.crop_year_id,
            base_purity=purity_prices_row.base_purity,
            base_purity_price=purity_prices_row.base_purity_price,
            price_difference=purity_prices_row.price_difference,

            # گرفتن فیلد از جدول دیگر
            crop_year_name=purity_prices_row.crop_year.crop_year_name if purity_prices_row.crop_year else None,

            created_at=to_jalali(purity_prices_row.created_at),
        )
        for purity_prices_row in purity_prices_results
    ]

    return paginate(result)

@router.delete('/{purity_price_id}')
def delete_seed(session: SessionDep, purity_price_id: int):
    get_pesticide = session.execute(
        select(PurityPrices).where(PurityPrices.id == purity_price_id)
    )

    result = get_pesticide.scalar_one_or_none()

    session.delete(result)
    session.commit()

    return f"Purity Price {purity_price_id} delete sucessfuly."