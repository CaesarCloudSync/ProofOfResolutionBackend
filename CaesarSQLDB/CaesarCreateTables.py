"""Table schema definitions and creation logic."""

from __future__ import annotations

from constants import (
    BIGINT_NOT_NULL,
    BLOCKCHAIN_PRIMARY_KEY,
    BLOCKCHAIN_TABLE,
    DATETIME_DEFAULT_NOW,
    DATETIME_NOT_NULL,
    GOAL_TABLE,
    GOALS_PRIMARY_KEY,
    VARCHAR_255_NOT_NULL,
    TEXT_NOT_NULL,
)
from CaesarSQLDB.CaesarCRUD import CaesarCRUD


class CaesarCreateTables:
    """Holds table metadata and creates all required tables."""

    # ------------------------------------------------------------------ blockchain
    CHAIN_FIELDS: tuple[str, ...] = (
        "index",
        "timestamp",
        "proof",
        "previous_hash",
        "block_hash",
    )
    CHAIN_TYPES: tuple[str, ...] = (
        BIGINT_NOT_NULL,
        DATETIME_NOT_NULL,
        BIGINT_NOT_NULL,
        VARCHAR_255_NOT_NULL,
        VARCHAR_255_NOT_NULL,
    )

    # ------------------------------------------------------------------ goals
    # NOTE: created_at is omitted from GOAL_FIELDS so we never have to pass it;
    # the DB fills it automatically via DEFAULT NOW().
    GOAL_FIELDS: tuple[str, ...] = (
        "goal_id",
        "title",
        "description",
        "category",
        "block_index",
        "block_hash",
    )
    GOAL_TYPES: tuple[str, ...] = (
        VARCHAR_255_NOT_NULL,   # goal_id  (UUID stored as text)
        VARCHAR_255_NOT_NULL,   # title
        TEXT_NOT_NULL,          # description
        VARCHAR_255_NOT_NULL,   # category
        BIGINT_NOT_NULL,        # block_index
        VARCHAR_255_NOT_NULL,   # block_hash
    )

    def create(self, crud: CaesarCRUD) -> None:
        """Initialise all required tables in the database."""
        crud.create_table(
            primary_key=BLOCKCHAIN_PRIMARY_KEY,
            fields=self.CHAIN_FIELDS,
            types=self.CHAIN_TYPES,
            table=BLOCKCHAIN_TABLE,
        )
        crud.create_table(
            primary_key=GOALS_PRIMARY_KEY,
            fields=self.GOAL_FIELDS,
            types=self.GOAL_TYPES,
            table=GOAL_TABLE,
        )