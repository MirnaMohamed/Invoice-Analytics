from typing import Union

from fastapi import FastAPI

from routers import user, invoices

app = FastAPI(
    swagger_ui_parameters={"useUnsafeMarkdown": True},
)

app.include_router(user.router)
app.include_router(invoices.router)


@app.get("/")
async def welcome():
    return {"message": "Hello World"}

