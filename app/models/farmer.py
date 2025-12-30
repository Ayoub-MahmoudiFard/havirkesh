from ..database import Base as SQLAlchemyBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, TIMESTAMP, ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime

class Farmers( SQLAlchemyBase ):
    __tablename__ = "farmer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    national_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    full_name: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    father_name: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    sheba_number_1: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    sheba_number_2: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    card_number: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    address: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now)