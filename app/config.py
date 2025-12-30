from fastapi import FastAPI

from .database import create_db_and_tables

# استفاده برای صفحه بندی
from fastapi_pagination import add_pagination

# Imports routers
from .routers import users
from .routers import provinces
from .routers import city
from .routers import village
from .routers import factory
from .routers import measure_unit
from .routers import pesticide
from .routers import seed
from .routers import product
from .routers import crop_year
from .routers import product_price
from .routers import purity_price
from .routers import farmer
from .routers import factory_seed
from .routers import factory_pesticide

app = FastAPI(
    title="ایوب محمودی فرد",
    description="پروژه کارشناسی ارشد - پایگاه داده پیشرفته",
    version="0.0.1",
)

# صفحه بندی
add_pagination(app)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(users.router)
app.include_router(provinces.router)
app.include_router(city.router)
app.include_router(village.router)
app.include_router(factory.router)
app.include_router(measure_unit.router)
app.include_router(pesticide.router)
app.include_router(seed.router)
app.include_router(product.router)
app.include_router(crop_year.router)
app.include_router(product_price.router)
app.include_router(purity_price.router)
app.include_router(farmer.router)
app.include_router(factory_seed.router)
app.include_router(factory_pesticide.router)