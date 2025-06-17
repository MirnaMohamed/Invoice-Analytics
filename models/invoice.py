from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel

from models.enums.currency import Currency


class Invoice(BaseModel):
    id: Optional[UUID] = uuid4()
    user_id : UUID
    amount : float
    original_currency : Currency
    Creation_Date: Optional[datetime] = datetime.now()
    converted_amount : float

    def __init__(self):
        converted_amount = 5


