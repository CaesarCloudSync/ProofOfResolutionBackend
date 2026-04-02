"""FastAPI application entry point."""

from __future__ import annotations

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from constants import CORS_HEADERS, CORS_METHODS, CORS_ORIGINS, LOG_LEVEL, SERVER_HOST, SERVER_PORT
from routers import auth_router, blockchain_router,resolution_router

# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    app = FastAPI(
        title="CaesarAI Blockchain API",
        description="A blockchain backed by PostgreSQL, exposed via FastAPI.",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=CORS_METHODS,
        allow_headers=CORS_HEADERS,
    )
    app.include_router(resolution_router)
    app.include_router(blockchain_router)
    app.include_router(auth_router)

    return app


app = create_app()


# ---------------------------------------------------------------------------
# Dev entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        log_level=LOG_LEVEL,
        reload=True,
    )