from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import documents, agents, health
from app.core.config import get_settings
from app.core.logging import setup_logging

def create_app() -> FastAPI:
    """
    Application factory.
    Facilita testes, escalabilidade e deploy profissional.
    """
    setup_logging()

    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        description="AI-powered document intelligence platform",
        version="0.1.0",
    )

    # =========================
    # CORS
    # =========================
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # =========================
    # Routers
    # =========================
    app.include_router(health.router)
    app.include_router(documents.router)
    app.include_router(agents.router)

    return app


app = create_app()
