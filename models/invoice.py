from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, DateTime

from db.database import Base
from dtos.currency import Currency

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    original_currency = Column(String, nullable=False)
    creation_date = Column(DateTime, default=datetime.now)

    converted_amount = Column(Float, nullable=True)

    def __init__(self, amount: float, original_currency: str, **kwargs):
        super().__init__(amount=amount, original_currency=original_currency, **kwargs)

        conversion_rates = {
            Currency.USD.value: 30.0,
            Currency.EUR.value: 33.0,
            Currency.GBP.value: 35.0,
        }
        rate = conversion_rates.get(original_currency, 1.0)
        self.converted_amount = amount * rate

    #@computed_field(return_type=float)
    #@property
    #def converted_amount(self) -> float:
    #    return self._converted_amount
    @property
    def standard_currency(self) -> Currency:
        return Currency.USD
