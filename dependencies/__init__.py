"""Dependency injection providers for FastAPI."""

from .dependencies import (
    get_crud,
    get_create_tables,
    get_blockchain,
    get_jwt_service,
    get_resolution_service
)

__all__ = [
    "get_crud",
    "get_create_tables",
    "get_blockchain",
    "get_jwt_service",
    "get_resolution_service"
]
