from datetime import datetime
from ..database import Base as SQLAlchemyBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, BigInteger, TIMESTAMP

class Users( SQLAlchemyBase ):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    fullname: Mapped['str'] = mapped_column(String, nullable=False)
    phone_number: Mapped['str'] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)
    role_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now)

    