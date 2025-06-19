from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, DateTime

from db.database import Base
from enums.currency import Currency

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    original_currency = Column(String, nullable=False)
    creation_date = Column(DateTime, default=datetime.now)

    converted_amount = Column(Float, nullable=True)
    exchange_rate: float = Column(Float, default=1, nullable=True)

    @property
    def standard_currency(self) -> Currency:
        return Currency.USD
