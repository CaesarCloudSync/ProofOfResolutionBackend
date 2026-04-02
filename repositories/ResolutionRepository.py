"""Resolution Repository – pure database layer."""

from __future__ import annotations

import uuid

from CaesarSQLDB.CaesarCRUD import CaesarCRUD
from CaesarSQLDB.CaesarCreateTables import CaesarCreateTables
from constants import GOAL_TABLE
from models.resolutions.dto.Resolution import Resolution


class ResolutionRepository:
    """Handles all database operations for resolutions."""

    def __init__(self, crud: CaesarCRUD, create_tables: CaesarCreateTables) -> None:
        self._crud = crud
        self._fields = create_tables.GOAL_FIELDS   # 6 fields, no created_at

    def create(
        self,
        title: str,
        description: str,
        category: str,
        block_index: int,
        block_hash: str,
    ) -> Resolution:
        """Persist a new resolution and return it as a DTO."""
        goal_id = str(uuid.uuid4())

        self._crud.post_data(
            fields=self._fields,           # (goal_id, title, description, category, block_index, block_hash)
            values=(goal_id, title, description, category, block_index, block_hash),
            table=GOAL_TABLE,
        )

        return Resolution(
            goal_id=goal_id,
            title=title,
            description=description,
            category=category,
            block_index=block_index,
            block_hash=block_hash,
        )

    def get_all(self) -> list[Resolution]:
        """Return all resolutions ordered by goal_id."""
        rows = self._crud.get_data(
            fields=self._fields,
            table=GOAL_TABLE,
            get_amount=1000,
            extra="ORDER BY goal_id ASC",
        )
        return [Resolution(**row) for row in rows]

    def get_by_id(self, goal_id: str) -> Resolution | None:
        """Return a single resolution by goal_id, or None."""
        rows = self._crud.get_data(
            fields=self._fields,
            table=GOAL_TABLE,
            condition=f"goal_id = '{goal_id}'",
            get_amount=1,
        )
        return Resolution(**rows[0]) if rows else None