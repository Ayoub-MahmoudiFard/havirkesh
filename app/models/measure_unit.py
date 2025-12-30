from ..database import Base as SQLAlchemyBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, TIMESTAMP, ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime

class MeasurUnites( SQLAlchemyBase ):
    __tablename__ = "measure_unit"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    unit_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now)

    pesticides = relationship("Pesticides", back_populates="measure_unit")
    seeds = relationship("Seeds", back_populates="measure_unit")
    products = relationship("Products", back_populates="measure_unit")
