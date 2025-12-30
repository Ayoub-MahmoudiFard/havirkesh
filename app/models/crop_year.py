from ..database import Base as SQLAlchemyBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, TIMESTAMP, ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime

class CropYears( SQLAlchemyBase ):
    __tablename__ = "crop_year"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    crop_year_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now)

    product_prices = relationship("ProductPrices", back_populates="crop_year")
    purity_price = relationship("PurityPrices", back_populates="crop_year")

    factory_seed = relationship("FactorySeeds", back_populates="crop_year")
    factory_pesticide = relationship("FactoryPesticides", back_populates="crop_year")