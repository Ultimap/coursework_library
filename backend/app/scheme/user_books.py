from datetime import date
from pydantic import BaseModel
from typing import Optional


class DateReturn(BaseModel):
    date_return: Optional[date] = None
