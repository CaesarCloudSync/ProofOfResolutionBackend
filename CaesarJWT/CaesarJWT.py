"""JWT authentication service."""

from __future__ import annotations

import hashlib

import jwt

from constants import (
    JWT_ALGORITHM,
    JWT_SECRET,
    STUDENT_SUBSCRIPTIONS_TABLE,
    USERS_TABLE,
)
from CaesarSQLDB.CaesarCRUD import CaesarCRUD
from models.auth.LoginRequest import LoginRequest
from models.auth.TokenPayload import TokenPayload
from models.auth.TokenResponse import TokenResponse


class CaesarJWT:
    """Handles JWT encoding / decoding and login verification."""

    def __init__(self, crud: CaesarCRUD) -> None:
        self._crud = crud

    # ------------------------------------------------------------------
    # Token helpers
    # ------------------------------------------------------------------

    def encode_token(self, payload: TokenPayload) -> str:
        """Return a signed JWT string for *payload*."""
        return jwt.encode(
            payload.model_dump(),
            JWT_SECRET,
            algorithm=JWT_ALGORITHM,
        )

    def decode_token(self, token: str) -> TokenPayload:
        """Decode and validate a JWT string, returning its payload."""
        data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return TokenPayload(**data)

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def provide_access_token(
        self,
        login: LoginRequest,
        is_student: bool = False,
    ) -> TokenResponse | None:
        """Validate credentials and return a *TokenResponse*, or *None* on failure."""
        table = STUDENT_SUBSCRIPTIONS_TABLE if is_student else USERS_TABLE
        condition = f"email = '{login.email}'"

        if not self._crud.check_exists(("*",), table, condition=condition):
            return None

        hashed_password = hashlib.sha256(login.password.encode("utf-8")).hexdigest()
        rows = self._crud.get_data(("email", "password"), USERS_TABLE, condition=condition)

        if not rows:
            return None

        user = rows[0]
        if user["password"] != hashed_password:
            return None

        payload = TokenPayload(email=user["email"])
        token = self.encode_token(payload)
        return TokenResponse(access_token=token)