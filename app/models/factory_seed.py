from ..database import Base as SQLAlchemyBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, TIMESTAMP, ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime

from decimal import Decimal

class FactorySeeds( SQLAlchemyBase ):
    __tablename__ = "factory_seed"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    factory_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("factory.id"),   # ← اتصال به factory
        nullable=False
    )
    seed_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("seed.id"),   # ← اتصال به seed
        nullable=False
    )
    crop_year_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("crop_year.id"),   # ← اتصال به crop_year
        nullable=False
    )

    amount: Mapped[Decimal] = mapped_column(String, unique=False, nullable=False)
    farmer_price: Mapped[Decimal] = mapped_column(String, unique=False, nullable=False)
    factory_price: Mapped[Decimal] = mapped_column(String, unique=False, nullable=False)

    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now)

    factories = relationship("Factories", back_populates="factory_seed")
    seeds = relationship("Seeds", back_populates="factory_seed")
    crop_year = relationship("CropYears", back_populates="factory_seed")
