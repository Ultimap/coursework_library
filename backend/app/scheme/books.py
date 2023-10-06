from pydantic import BaseModel
from datetime import date
from typing import Optional

class StyleScheme(BaseModel):
    name: str


class AuthorScheme(BaseModel):
    name: Optional[str] = None
    birth_data: Optional[date] = None
    death_data: Optional[date] = None


class BookEdit(BaseModel):
    name: Optional[str]= None
    description: Optional[str] = None
    count: Optional[int] = None
    style: Optional[int] = None
    author: Optional[int] = None
    age_restriction: Optional[int] = None
    release_date: Optional[date] = None
