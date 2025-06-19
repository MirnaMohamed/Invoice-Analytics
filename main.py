from fastapi import FastAPI

from core.config import settings
from db.database import engine
from models import invoice
from routers.analytics import analytics_router
from routers.invoices import router as invoice_router
from services.exchange_rate import router as exchange_router

def include_router(base_app):
    base_app.include_router(analytics_router)
    base_app.include_router(invoice_router)
    base_app.include_router(exchange_router)

def on_startup():
    invoice.Base.metadata.create_all(bind=engine)

def start_application():
    app_builder = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION
    )
    include_router(app_builder)
    return app_builder

app = start_application()


@app.get("/")
async def welcome():
    return {"message": "Hello World"}

