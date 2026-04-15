import structlog
from fastapi import FastAPI

from app.api import health, products, sales
from app.config import settings

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.dev.ConsoleRenderer() if settings.debug else structlog.processors.JSONRenderer(),
    ],
)

app = FastAPI(
    title=settings.app_name,
    description="Backend for local businesses: inventory, sales, alerts, forecasting",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(health.router)
app.include_router(products.router, prefix="/api/v1")
app.include_router(sales.router, prefix="/api/v1")
