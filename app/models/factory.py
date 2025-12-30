from ..database import Base as SQLAlchemyBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, TIMESTAMP, ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime

class Factories( SQLAlchemyBase ):
    __tablename__ = "factory"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    factory_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now)

    factory_seed = relationship("FactorySeeds", back_populates="factories")
    factory_pesticide = relationship("FactoryPesticides", back_populates="factories")
