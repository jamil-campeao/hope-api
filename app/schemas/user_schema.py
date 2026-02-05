from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreateRequest(BaseModel):
    email: str
    name: str
    password: str
    phone: str

class UserUpdateRequest(BaseModel):
    id: int
    email: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    active: Optional[bool] = None

class UserUpdatePasswordRequest(BaseModel):
    id: int
    new_password: str
    old_password: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    phone: str
    is_active: bool
    created_at: datetime
    updated_at: datetime | None
