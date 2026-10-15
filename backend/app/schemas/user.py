from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    emailOrPhone: str = Field(min_length=5, max_length=254)
    password: str = Field(min_length=8)
    role: Literal["farmer", "buyer"]


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    emailOrPhone: str | None = Field(default=None, min_length=5, max_length=254)


class UserResponse(BaseModel):
    id: str
    name: str
    emailOrPhone: str
    role: str
    createdAt: datetime
