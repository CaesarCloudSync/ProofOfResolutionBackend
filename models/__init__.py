"""Pydantic request/response models (DTOs) for the application."""

from .resolutions.requests import ResolutionCreate

from .blockchain import (
    BlockDTO,
    MineBlockResponse,
    GetChainResponse,
    ValidityResponse,
)

from .auth import (
    LoginRequest,
    TokenResponse,
    TokenPayload,
)

from .error import ErrorResponse

from .resolutions.dto import Resolution
from .resolutions.responses import GetAllResolutionsResponse, CreateResolutionResponse
__all__ = [
    "BlockDTO",
    "MineBlockResponse",
    "GetChainResponse",
    "ValidityResponse",
    "LoginRequest",
    "TokenResponse",
    "TokenPayload",
    "ErrorResponse",
    "Resolution",
    "ResolutionCreate"
]