"""CRUD operations built on top of CaesarSQL."""

from __future__ import annotations

import base64
from typing import Any, Generator, Optional

from CaesarSQLDB.CaesarSQL import CaesarSQL


class CaesarCRUD:
    """High-level CRUD interface."""

    def __init__(self) -> None:
        self._sql = CaesarSQL()

    # ------------------------------------------------------------------
    # Schema helpers
    # ------------------------------------------------------------------

    def create_table(
        self,
        primary_key: str,
        fields: tuple[str, ...],
        types: tuple[str, ...],
        table: str,
    ) -> Optional[dict[str, str]]:
        """Create *table* if it does not already exist."""
        field_defs = ", ".join(
            f'"{field}" {type_}' for field, type_ in zip(fields, types)
        )
        # Quote primary key too in case it's a reserved word
        sql = (
            f'CREATE TABLE IF NOT EXISTS {table} '
            f'("{primary_key}" INTEGER PRIMARY KEY AUTOINCREMENT, {field_defs});'
        )
        self._sql.run_command(sql, self._sql.fetch)
        return {"message": f"{table} table ensured."}

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    def post_data(
        self,
        fields: tuple[str, ...],
        values: tuple[Any, ...],
        table: str,
    ) -> bool:
        """Insert a row and return *True* on success."""
        field_str = self._build_field_str(fields)
        placeholders = ", ".join(["?"] * len(values))
        sql = f"INSERT INTO {table} ({field_str}) VALUES ({placeholders});"
        self._sql.run_command(sql, self._sql.fetch, datatuple=values)
        return True  # SQLite INSERT doesn't return rows; no error = success

    def update_data(
        self,
        fields_to_update: tuple[str, ...],
        values: tuple[Any, ...],
        table: str,
        condition: str,
    ) -> bool:
        """Update columns matching *condition* and return *True* on success."""
        set_parts = []
        for field, value in zip(fields_to_update, values):
            if isinstance(value, str):
                value = value.replace("'", "''")
                set_parts.append(f'"{field}" = \'{value}\'')
            else:
                set_parts.append(f'"{field}" = {value}')
        set_clause = ", ".join(set_parts)
        sql = f"UPDATE {table} SET {set_clause} WHERE {condition};"
        self._sql.run_command(sql, self._sql.fetch)
        return True

    def delete_data(self, table: str, condition: str) -> bool:
        """Delete rows matching *condition* and return *True* on success."""
        sql = f"DELETE FROM {table} WHERE {condition};"
        self._sql.run_command(sql, self._sql.fetch)
        return True

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    def get_data(
        self,
        fields: tuple[str, ...],
        table: str,
        condition: Optional[str] = None,
        get_amount: int = 1000,
        extra: str = "",
    ) -> list[dict[str, Any]]:
        """Fetch rows and return them as a list of plain dicts."""
        field_str = self._build_field_str(fields)

        if condition:
            sql = f"SELECT {field_str} FROM {table} WHERE {condition} LIMIT {get_amount};"
        else:
            sql = f"SELECT {field_str} FROM {table} {extra} LIMIT {get_amount};"

        result = self._sql.run_command(sql, self._sql.fetch)
        if not result:
            return []

        return self._rows_to_dicts(fields, result)

    def get_large_data(
        self,
        fields: tuple[str, ...],
        table: str,
        condition: Optional[str] = None,
    ) -> Generator[Any, None, None]:
        """Streaming read for large result sets."""
        field_str = self._build_field_str(fields)
        if condition:
            sql = f"SELECT {field_str} FROM {table} WHERE {condition};"
        else:
            sql = f"SELECT {field_str} FROM {table};"
        return self._sql.run_command_generator(sql)

    def check_exists(
        self,
        fields: tuple[str, ...],
        table: str,
        condition: Optional[str] = None,
    ) -> bool:
        """Return *True* when at least one matching row exists."""
        field_str = self._build_field_str(fields)
        if condition:
            sql = f"SELECT {field_str} FROM {table} WHERE {condition};"
        else:
            sql = f"SELECT {field_str} FROM {table};"
        return self._sql.run_command(sql, self._sql.check_exists)

    # ------------------------------------------------------------------
    # Binary helpers
    # ------------------------------------------------------------------

    def update_blob(
        self,
        field_to_update: str,
        value: str,
        table: str,
        condition: str,
    ) -> bool:
        hex_value = self._base64_to_hex(value)
        sql = (
            f'UPDATE {table} SET "{field_to_update}" = X\'{hex_value}\' '
            f"WHERE {condition};"
        )
        self._sql.run_command(sql, self._sql.fetch)
        return True

    @staticmethod
    def hex_to_base64(hex_bytes: bytes) -> str:
        return base64.b64encode(bytes.fromhex(hex_bytes.hex())).decode()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _base64_to_hex(value: str) -> str:
        return base64.decodebytes(value.encode()).hex()

    @staticmethod
    def _build_field_str(fields: tuple[str, ...]) -> str:
        """Build a quoted, comma-separated field list safe for SQLite reserved words."""
        if fields == ("*",):
            return "*"
        return ", ".join(f'"{f}"' for f in fields)

    @staticmethod
    def _rows_to_dicts(
        fields: tuple[str, ...], rows: list[Any]
    ) -> list[dict[str, Any]]:
        """Convert raw sqlite row tuples into plain dicts keyed by field name."""
        if not rows:
            return []

        first = rows[0]
        # Multi-column: each row is a tuple
        if isinstance(first, (tuple, list)):
            return [dict(zip(fields, row)) for row in rows]
        # Single-column: each row is a scalar
        return [{fields[0]: row} for row in rows]