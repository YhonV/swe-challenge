from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.v1.users_controller import router
from app.db.database import engine, Base
from app.core.logging import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="User Management API",
    description="RESTful API for user management",
    version="1.0",
    lifespan=lifespan
)
logger.info("Starting User Management API")
app.include_router(router, prefix="/api/v1")
