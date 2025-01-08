from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import chat, health, ingest, auth
from app.core.config import Settings
from app.core.logging import configure_logging
from app.core.metrics import MetricsMiddleware

settings = Settings()
configure_logging(settings.log_level)

app = FastAPI(title=settings.app_name, version=settings.version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"]
    ,
    allow_headers=["*"]
)
app.add_middleware(MetricsMiddleware)

app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(ingest.router, prefix="/api/v1/ingest", tags=["ingest"])


@app.on_event("startup")
async def on_startup() -> None:
    settings.validate_runtime()
