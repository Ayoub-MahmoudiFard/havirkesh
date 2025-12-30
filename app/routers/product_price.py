from fastapi import APIRouter, HTTPException
from fastapi import APIRouter
from ..database import SessionDep
from ..schemas.product_price import ProductPriceSchema, Filters, ProductPriceCreate
from ..models.product_price import ProductPrices

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

router = APIRouter(prefix='/product_price', tags=["Product Price"])

@router.post("/")
def create_product_price(session: SessionDep, product_price_param: ProductPriceCreate):

    product_price_insert = ProductPrices(
        crop_year_id = product_price_param.crop_year_id,
        sugar_amount_per_ton_kg = product_price_param.sugar_amount_per_ton_kg,
        sugar_price_per_kg = product_price_param.sugar_price_per_kg,
        pulp_amount_per_ton_kg = product_price_param.pulp_amount_per_ton_kg,
        pulp_price_per_kg = product_price_param.pulp_price_per_kg,
    )

    session.add(product_price_insert)
    session.commit()
    session.refresh(product_price_insert)

    return {
        "id": product_price_insert.id,
        "crop_year_id": product_price_insert.crop_year_id,
        "sugar_amount_per_ton_kg": product_price_insert.sugar_amount_per_ton_kg,
        "sugar_price_per_kg": product_price_insert.sugar_price_per_kg,
        "pulp_amount_per_ton_kg": product_price_insert.pulp_amount_per_ton_kg,
        "pulp_price_per_kg": product_price_insert.pulp_price_per_kg,
        # گرفتن فیلد از جدول دیگر
        "crop_year_name": (
            product_price_insert.crop_year.crop_year_name
            if product_price_insert.crop_year else None
        )
    }

@router.get("/")
def select_all_product_price(session: SessionDep
    , filters: Filters = Depends()) -> Page[ProductPriceSchema]:

    # وصل کردن دو جدول به هم
    query = select(ProductPrices).options(
        joinedload(ProductPrices.crop_year)
    )
    
    if filters.crop_year_id:
        query = query.where(
            or_(
                ProductPrices.crop_year_id == int(filters.crop_year_id)
            )
        )

    if filters.sort_by:
        column = getattr(ProductPrices, filters.sort_by, None)
        if column is None:
            raise HTTPException(status_code=400, detail="Invalid sort field")

        if filters.sort_order.lower() == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

    product_prices_results = session.execute(query).scalars().all()

    if not product_prices_results:
        raise HTTPException(status_code=404, detail="Recrod not found")
    
    result = [
        ProductPriceSchema(
            id=product_prices_row.id,
            crop_year_id=product_prices_row.crop_year_id,
            sugar_amount_per_ton_kg=product_prices_row.sugar_amount_per_ton_kg,
            sugar_price_per_kg=product_prices_row.sugar_price_per_kg,
            pulp_amount_per_ton_kg=product_prices_row.pulp_amount_per_ton_kg,
            pulp_price_per_kg=product_prices_row.pulp_price_per_kg,

            # گرفتن فیلد از جدول دیگر
            crop_year_name=product_prices_row.crop_year.crop_year_name if product_prices_row.crop_year else None,

            created_at=to_jalali(product_prices_row.created_at),
        )
        for product_prices_row in product_prices_results
    ]

    return paginate(result)

@router.delete('/{product_price}')
def delete_seed(session: SessionDep, product_price_id: int):
    get_pesticide = session.execute(
        select(ProductPrices).where(ProductPrices.id == product_price_id)
    )

    result = get_pesticide.scalar_one_or_none()

    session.delete(result)
    session.commit()

    return f"product Price {product_price_id} delete sucessfuly."