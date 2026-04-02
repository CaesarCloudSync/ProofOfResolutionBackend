"""Application-wide constants."""

import os

# Database – SQLite file path (no external server needed)
DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "app.db",
)

# JWT
JWT_SECRET: str = (
    "Peter Piper picked a peck of pickled peppers, "
    "A peck of pickled peppers Peter Piper picked, "
    "If Peter Piper picked a peck of pickled peppers,"
    "Where's the peck of pickled peppers Peter Piper picked"
)
JWT_ALGORITHM: str = "HS256"

# Blockchain
BLOCKCHAIN_TABLE: str = "blockchain"
GOAL_TABLE: str = "goals"
GOALS_PRIMARY_KEY: str = "goalid"
BLOCKCHAIN_PRIMARY_KEY: str = "blockchainid"
PROOF_OF_WORK_PREFIX: str = "0000"

# Users
USERS_TABLE: str = "users"
STUDENT_SUBSCRIPTIONS_TABLE: str = "studentsubscriptions"

# DB field types (SQLite-compatible)
BIGINT_NOT_NULL: str = "INTEGER NOT NULL"
DATETIME_NOT_NULL: str = "TEXT NOT NULL"
DATETIME_DEFAULT_NOW: str = "TEXT NOT NULL DEFAULT (datetime('now'))"
VARCHAR_255_NOT_NULL: str = "TEXT NOT NULL"
TEXT_NOT_NULL: str = "TEXT NOT NULL"

# CORS
CORS_ORIGINS: list[str] = ["*"]
CORS_METHODS: list[str] = ["*"]
CORS_HEADERS: list[str] = ["*"]

# Server
SERVER_HOST: str = "0.0.0.0"
SERVER_PORT: int = 8080
LOG_LEVEL: str = "info"