from ..database import Base as SQLAlchemyBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, TIMESTAMP, ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime

class ProductPrices( SQLAlchemyBase ):
    __tablename__ = "product_price"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    crop_year_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("crop_year.id"),   # ← اتصال به crop_year
        nullable=False
    )

    sugar_amout_per_ton_kg: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    sugar_price_per_kg: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    pulb_amout_per_ton_kg: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    pulb_amout_per_kg: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now)

    crop_year = relationship("CropYears", back_populates="product_prices")
