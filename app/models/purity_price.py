from ..database import Base as SQLAlchemyBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, TIMESTAMP, ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime

from decimal import Decimal

class PurityPrices( SQLAlchemyBase ):
    __tablename__ = "purity_price"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    crop_year_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("crop_year.id"),   # ← اتصال به crop_year
        nullable=False
    )

    base_purity: Mapped[int] = mapped_column(String, unique=False, nullable=False)
    base_purity_price: Mapped[Decimal] = mapped_column(String, unique=False, nullable=False)
    price_difference: Mapped[Decimal] = mapped_column(String, unique=False, nullable=False)
    
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now)

    crop_year = relationship("CropYears", back_populates="purity_price")
