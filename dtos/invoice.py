from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from dtos.currency import Currency

class CreateInvoiceDTO(BaseModel):
    amount: float = Field(gt=0, description="Invoice amount")
    original_currency: Optional[Currency] = Currency.USD
    creation_date: Optional[datetime] = None


class GetInvoiceDTO(BaseModel):
    id: int
    amount: float
    original_currency: Currency
    creation_date: datetime
    converted_amount: float
    standard_currency: Currency