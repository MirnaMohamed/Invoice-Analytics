from typing import List

from fastapi import APIRouter

from models.invoice import Invoice

router = APIRouter()
#endpoint_name = "invoices"

invoices: List[Invoice] = [

]

@router.get("/invoices", response_model=List[Invoice])
async def read_invoices():
    return invoices

@router.get("/invoices/{invoice_id}", response_model=Invoice)
async def get_invoice_by_id(invoice_id: int):
    return invoices[invoice_id]

@router.post("/invoices", response_model=Invoice)
async def create_invoice(invoice: Invoice):
    invoices.append(invoice)
    return invoice

@router.put("/invoices/{id}", response_model=Invoice)
async def update_invoice(id: int, invoice: Invoice):
    invoices[id] = invoice
    return invoice

@router.delete("/invoices/{invoice_id}")
async def delete_invoice(invoice_id: int):
    del invoices[invoice_id]
    return {"message": "Invoice deleted"}
