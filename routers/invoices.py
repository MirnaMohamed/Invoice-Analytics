from datetime import datetime
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from dtos.invoice import CreateInvoiceDTO, GetInvoiceDTO
from models.invoice import Invoice
from services.exchange_rate import get_latest_exchange_rate, old_exchange_rate

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/")
def read_invoices(db: Session = Depends(get_db)):
    return db.query(Invoice).all()

# GET invoice by ID
@router.get("/{invoice_id}")
async def get_invoice_by_id(invoice_id: int, db: db_dependency):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=404,
            detail=f"Invoice with id: {invoice_id} not found"
        )
    return invoice

# POST create new invoice
@router.post("/", status_code=HTTPStatus.CREATED, response_model=GetInvoiceDTO)
async def create_invoice(dto: CreateInvoiceDTO, db: db_dependency):
    rate: float = 0
    if dto.creation_date < datetime.today():
        rate = await old_exchange_rate(dto.original_currency, dto.creation_date)
    elif dto.creation_date > datetime.now():
        raise HTTPException(status_code=400, detail="Creation date cannot be in the future.")
    else:
        rates = await get_latest_exchange_rate()
        rate = rates.get(dto.original_currency)
    if rate is None:
        raise HTTPException(status_code=400, detail="Unsupported currency")

    converted_amount = dto.amount / rate

    invoice = Invoice(
        amount=dto.amount,
        original_currency=dto.original_currency,
        exchange_rate= rate,
        converted_amount=converted_amount
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return GetInvoiceDTO.model_validate(invoice)

# PUT update invoice
@router.put("/{invoice_id}",
            status_code=HTTPStatus.OK, response_model=GetInvoiceDTO)
async def update_invoice(invoice_id: int, dto: CreateInvoiceDTO, db: db_dependency):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=404,
            detail=f"Invoice with id: {invoice_id} not found"
        )
    for key, value in dto.model_dump().items():
        setattr(invoice, key, value)
    db.commit()
    db.refresh(invoice)
    return GetInvoiceDTO(**invoice.__dict__)

# DELETE invoice
@router.delete("/{invoice_id}", status_code=HTTPStatus.OK)
async def delete_invoice(invoice_id: int, db: db_dependency):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=404,
            detail=f"Invoice with id: {invoice_id} not found"
        )
    db.delete(invoice)
    db.commit()
    return {"message": "Invoice deleted"}
