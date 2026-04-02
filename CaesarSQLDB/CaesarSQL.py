"""Low-level SQLite connection and command execution."""

from __future__ import annotations

import json
import os
import sqlite3
from typing import Any, Callable, Generator, Optional

# Absolute path to app.db — always in the project root regardless of cwd
_DB_PATH = "/tmp/app.db"


class CaesarSQL:
    """Manages a single sqlite3 connection and exposes helpers for executing SQL."""

    def __init__(self) -> None:
        print(f"[CaesarSQL] Connecting to SQLite at: {_DB_PATH}")
        # Ensure the directory exists and is writable

        self.connection: sqlite3.Connection = sqlite3.connect(
            _DB_PATH, check_same_thread=False
        )
        self.connection.row_factory = sqlite3.Row
        self.connection.isolation_level = None  # autocommit

    def check_exists(self, result: list[Any]) -> bool:
        try:
            return len(result) > 0
        except Exception:
            return False

    def fetch(self, result: list[Any]) -> list[Any]:
        return result

    def load_json_file(self, filename: str) -> Any:
        with open(filename) as f:
            return json.load(f)

    def run_command(
        self,
        sql: str,
        result_function=None,
        datatuple=None,
        filename=None,
        verbose: int = 0,
    ) -> Any:
        if sql is None and filename is None:
            raise ValueError("Provide either sql or filename.")
        if filename is not None:
            with open(filename) as f:
                sql = f.read()

        cursor = self.connection.cursor()
        if datatuple:
            cursor.execute(sql, datatuple )
        else:
            cursor.execute(sql)
        try:
            rows = cursor.fetchall()
            rows = [tuple(row) for row in rows]
        except Exception:
            rows = []

        result = result_function(rows) if result_function is not None else None
        if verbose:
            print("SQL command executed.")
        return result

    def run_command_generator(
        self,
        sql: str,
        arraysize: int = 1000,
        datatuple=None,
        filename=None,
        verbose: int = 1,
    ) -> Generator[Any, None, None]:
        if sql is None and filename is None:
            raise ValueError("Provide either sql or filename.")
        if filename is not None:
            with open(filename) as f:
                sql = f.read()

        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, datatuple or ())
            if verbose:
                print("SQL command executed.")
            while True:
                rows = cursor.fetchmany(arraysize)
                if not rows:
                    break
                yield from (tuple(row) for row in rows)
        except Exception as exc:
            print(f"{type(exc).__name__}: {exc}")