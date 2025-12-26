"""Module with FastAPI application"""

from fastapi import FastAPI

from .api.v1.router import router

app = FastAPI(
    title="HMAC-Python",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)
app.include_router(router, prefix="/api/v1")
