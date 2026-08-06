from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.init_db import initialize_database
from app.routes import router
from app.utils import configure_logging


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    initialize_database()
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="AI assistant that converts natural language questions into SQLite queries.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check() -> dict[str, str | bool]:
    return {"success": True, "message": "AI SQL Assistant API is running"}


app.include_router(router)
