from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from dtos.invoice import CreateInvoiceDTO, GetInvoiceDTO
from models.invoice import Invoice

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
    invoice = Invoice(**dto.model_dump())
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return GetInvoiceDTO(**invoice.__dict__)

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
