from fastapi import FastAPI

from .routers.health import router as health_router
from .routers.tours import router as tours_router
from .routers.orders import router as orders_router

app = FastAPI(
    title="Tourism WebApp (Case 4)",
    version="1.0.0",
)

app.include_router(health_router)
app.include_router(tours_router)
app.include_router(orders_router)
