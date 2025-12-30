from ..database import Base as SQLAlchemyBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, TIMESTAMP, ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime

class Cities( SQLAlchemyBase ):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    province_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("province.id"),   # ← اتصال به Provinces
        nullable=False
    )

    city: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now)

    province = relationship("Provinces", back_populates="cities")
    villages = relationship("Villages", back_populates="city")
