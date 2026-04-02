"""Hashing utilities."""

from __future__ import annotations

import hashlib
import uuid


class CaesarHash:
    """Static hashing helpers used throughout the application."""

    @staticmethod
    def hash_text_auth(text: str) -> str:
        """Hash *text* with a random salt; returns ``'<hash>:<salt>'``."""
        salt = uuid.uuid4().hex
        hashed = hashlib.sha256((salt + text).encode()).hexdigest()
        return f"{hashed}:{salt}"

    @staticmethod
    def hash_text(text: str) -> str:
        """Return a plain SHA-256 hex digest of *text*."""
        return hashlib.sha256(text.encode()).hexdigest()

    @staticmethod
    def match_hashed_text(hashed_text: str, provided_text: str) -> bool:
        """Return *True* when *provided_text* matches the salted *hashed_text*."""
        stored_hash, salt = hashed_text.split(":")
        candidate = hashlib.sha256((salt + provided_text).encode()).hexdigest()
        return stored_hash == candidate

    @staticmethod
    def hash_quota(data: dict[str, str]) -> str:
        """Derive a deterministic hash for a quota record."""
        raw = (
            data["quotatitle"].lower().replace(" ", "")
            + data["quotatype"].lower().replace(" ", "")
        )
        return CaesarHash.hash_text(raw)