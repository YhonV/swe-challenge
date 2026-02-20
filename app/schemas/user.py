import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.db.models import UserRole
from datetime import datetime

class UserBase(BaseModel):
    username:   str = Field(min_length=3, max_length=50)
    email:      str
    first_name: str = Field(min_length=1, max_length=100)
    last_name:  str = Field(min_length=1, max_length=100)
    role:       UserRole
    active:     bool

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        import re
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', v):
            raise ValueError('Invalid email format')
        return v

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username:   Optional[str] = None
    email:      Optional[str] = None
    first_name: Optional[str] = None
    last_name:  Optional[str] = None
    role:       Optional[UserRole] = None
    active:     Optional[bool] = None

class UserResponse(UserBase):
    id:         uuid.UUID
    created_at: datetime
    updated_at: datetime
    active:     bool
    model_config = ConfigDict(from_attributes=True)
    pass
