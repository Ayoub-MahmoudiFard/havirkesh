from fastapi import APIRouter, HTTPException
from fastapi import APIRouter
from ..database import SessionDep
from ..schemas.product import ProductSchema, Filters, ProductCreate
from ..models.product import Products

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

router = APIRouter(prefix='/product', tags=["Product"])

@router.post("/")
def create_product(session: SessionDep, product_param: ProductCreate):

    product_insert = Products(
        product_name = product_param.product_name,
        measure_unit_id = product_param.measure_unit_id
    )

    session.add(product_insert)
    session.commit()
    session.refresh(product_insert)

    return {
        "id": product_insert.id,
        "product_name": product_insert.product_name,
        "measure_unit_id": product_insert.measure_unit_id,
        # گرفتن فیلد از جدول دیگر
        "unit_name": (
            product_insert.measure_unit.unit_name
            if product_insert.measure_unit else None
        ),

        "created_at": to_jalali(product_insert.created_at)
    }

@router.get("/")
def select_all_product(session: SessionDep
    , filters: Filters = Depends()) -> Page[ProductSchema]:

    # وصل کردن دو جدول به هم
    query = select(Products).options(
        joinedload(Products.measure_unit)
    )
    
    if filters.search:
        query = query.where(
            or_(
                Products.product_name.ilike(f"%{filters.search}%"),
            )
        )

    if filters.sort_by:
        column = getattr(Products, filters.sort_by, None)
        if column is None:
            raise HTTPException(status_code=400, detail="Invalid sort field")

        if filters.sort_order.lower() == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

    product_results = session.execute(query).scalars().all()

    if not product_results:
        raise HTTPException(status_code=404, detail="Record not found")
    
    result = [
        ProductSchema(
            id=product_row.id,
            measure_unit_id=product_row.measure_unit_id,
            product_name=product_row.product_name,

            # گرفتن فیلد از جدول دیگر
            measure_unit_name=product_row.measure_unit.unit_name if product_row.measure_unit else None,

            created_at=to_jalali(product_row.created_at),
        )
        for product_row in product_results
    ]

    return paginate(result)

@router.delete('/{product}')
def delete_seed(session: SessionDep, product_name: str):
    get_product = session.execute(
        select(Products).where(Products.product_name == product_name)
    )

    result = get_product.scalar_one_or_none()

    session.delete(result)
    session.commit()

    return f"product {product_name} delete sucessfuly."