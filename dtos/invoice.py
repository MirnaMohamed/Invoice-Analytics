from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from enums.currency import Currency

class CreateInvoiceDTO(BaseModel):
    amount: float = Field(gt=0, description="Invoice amount")
    original_currency: Optional[Currency] = Currency.USD
    customer_name: Optional[str] = None
    creation_date: Optional[datetime] = datetime.now()


class GetInvoiceDTO(BaseModel):
    id: int
    amount: float
    original_currency: Currency
    creation_date: datetime
    converted_amount: float
    standard_currency: Currency
    exchange_rate: float

    model_config = ConfigDict(from_attributes=True)