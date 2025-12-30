from ..database import Base as SQLAlchemyBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, TIMESTAMP, ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime

class Pesticides( SQLAlchemyBase ):
    __tablename__ = "pesticide"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    measure_unit_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("measure_unit.id"),   # ← اتصال به measure_unit
        nullable=False
    )

    pesticide_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now)

    measure_unit = relationship("MeasurUnites", back_populates="pesticides")
    factory_pesticide = relationship("FactoryPesticides", back_populates="pesticides")
