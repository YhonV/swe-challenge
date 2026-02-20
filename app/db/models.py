import uuid
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import enum
from app.db.database import Base
from sqlalchemy import Date, DateTime, func
from datetime import date, datetime

class UserRole(str, enum.Enum):
    admin = "admin"
    user  = "user"
    guest = "guest"

class User(Base):
    __tablename__ = "users"

    id:         Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username:   Mapped[str]
    email:      Mapped[str]
    first_name: Mapped[str]
    last_name:  Mapped[str]
    role:       Mapped[UserRole]
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    active:     Mapped[bool] = mapped_column(default=True)



