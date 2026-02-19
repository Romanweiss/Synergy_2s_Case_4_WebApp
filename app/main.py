from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import run_startup_migrations
from .routers.health import router as health_router
from .routers.services import router as services_router
from .routers.tours import router as tours_router
from .routers.orders import router as orders_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    run_startup_migrations()
    yield


app = FastAPI(
    title="Tourism WebApp (Case 4)",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(services_router)
app.include_router(tours_router)
app.include_router(orders_router)
