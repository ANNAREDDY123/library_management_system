from pydantic import BaseModel, Field
from typing import Optional
import re

class MemberCreate(BaseModel):
    name: str
    email: str
    phone: str

    @classmethod
    def validate_phone(cls, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must contain exactly 10 digits")
        return value

class MemberUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class BookCreate(BaseModel):
    title: str = Field(min_length=2)
    author: str
    category: str
    available_copies: int

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    available_copies: Optional[int] = None

class BorrowCreate(BaseModel):
    book_id: int
    member_id: int
