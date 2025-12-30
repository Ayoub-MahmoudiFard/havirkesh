from ..database import Base as SQLAlchemyBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, TIMESTAMP, ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime

class Villages( SQLAlchemyBase ):
    __tablename__ = "village"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    city_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("city.id"),   # ← اتصال به City
        nullable=False
    )

    village: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now)

    city = relationship("Cities", back_populates="villages")
