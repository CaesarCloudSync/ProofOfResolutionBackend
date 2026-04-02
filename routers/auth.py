"""Authentication API router."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from CaesarJWT.CaesarJWT import CaesarJWT
from dependencies import get_jwt_service
from models.auth.LoginRequest import LoginRequest
from models.auth.TokenResponse import TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate and receive a JWT",
)
def login(
    payload: LoginRequest,
    jwt_service: CaesarJWT = Depends(get_jwt_service),
) -> TokenResponse:
    """Validate credentials and return a bearer token."""
    token_response = jwt_service.provide_access_token(payload)
    if token_response is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )
    return token_response


@router.post(
    "/login/student",
    response_model=TokenResponse,
    summary="Authenticate a student and receive a JWT",
)
def login_student(
    payload: LoginRequest,
    jwt_service: CaesarJWT = Depends(get_jwt_service),
) -> TokenResponse:
    """Validate student credentials and return a bearer token."""
    token_response = jwt_service.provide_access_token(payload, is_student=True)
    if token_response is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )
    return token_response