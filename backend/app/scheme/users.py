from pydantic import BaseModel
from typing import Optional


class UserScheme(BaseModel):
    username: Optional[str] = None
    age: Optional[int] = None
    password: Optional[str] = None


