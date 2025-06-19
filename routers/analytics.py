from datetime import datetime
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from db.database import get_db
from models.invoice import Invoice

analytics_router = APIRouter(prefix="/analytics", tags=["Analytics"])

@analytics_router.get("/monthly-revenue")
def get_monthly_revenue(year: int, db: Session = Depends(get_db)):
    results = (
        db.query(
            extract('month', Invoice.creation_date).label("month"),
            func.sum(Invoice.converted_amount).label("total")
        )
        .filter(extract('year', Invoice.creation_date) == year)
        .group_by("month")
        .order_by("month")
        .all()
    )
    return [{"month": int(row.month), "revenue": float(row.total)} for row in results]

@analytics_router.get("/total-revenue")
def get_total_revenue(start_date: str, end_date: str, db: Session = Depends(get_db)):
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)

    total = (
        db.query(func.sum(Invoice.converted_amount))
        .filter(Invoice.creation_date >= start, Invoice.creation_date <= end)
        .scalar()
    )

    return {"total_revenue": float(total or 0)}