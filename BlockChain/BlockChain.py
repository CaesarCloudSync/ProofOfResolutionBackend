"""Blockchain business logic."""

from __future__ import annotations

import datetime
import hashlib
import json

from constants import BLOCKCHAIN_TABLE, PROOF_OF_WORK_PREFIX
from CaesarSQLDB.CaesarCRUD import CaesarCRUD
from CaesarSQLDB.CaesarCreateTables import CaesarCreateTables
from models.blockchain.BlockDTO import BlockDTO


class BlockChain:
    """Append-only blockchain persisted to PostgreSQL."""

    def __init__(self, crud: CaesarCRUD, create_tables: CaesarCreateTables) -> None:
        self._crud = crud
        self._fields = create_tables.CHAIN_FIELDS
        self._create_genesis_block()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_last_block(self) -> BlockDTO:
        rows = self._crud.get_data(
            fields=self._fields,
            table=BLOCKCHAIN_TABLE,
            get_amount=1,
            extra='ORDER BY "index" DESC',
        )
        if not rows:
            raise RuntimeError("Blockchain is empty – genesis block missing.")
        return BlockDTO(**rows[0])

    def create_block(self, proof: int, previous_hash: str) -> BlockDTO:
        """Append a new block and return it as a DTO."""
        rows = self._crud.get_data(
            fields=self._fields,
            table=BLOCKCHAIN_TABLE,
            get_amount=1,
            extra='ORDER BY "index" DESC',
        )
        last_index: int = rows[0]["index"] if rows else 0

        timestamp = str(datetime.datetime.now(tz=datetime.timezone.utc))

        # Build the raw dict we want to hash (no block_hash yet)
        raw = {
            "index": last_index + 1,
            "timestamp": timestamp,
            "proof": proof,
            "previous_hash": previous_hash,
        }
        block_hash = hashlib.sha256(
            json.dumps(raw, sort_keys=True).encode()
        ).hexdigest()

        block_data = {**raw, "block_hash": block_hash}

        self._crud.post_data(
            fields=self._fields,
            values=(
                block_data["index"],
                block_data["timestamp"],
                block_data["proof"],
                block_data["previous_hash"],
                block_data["block_hash"],
            ),
            table=BLOCKCHAIN_TABLE,
        )

        return BlockDTO(**block_data)

    def proof_of_work(self, previous_proof: int) -> int:
        """Find a nonce satisfying the difficulty target."""
        new_proof = 1
        while True:
            candidate = new_proof ** 2 - previous_proof ** 2
            hash_result = hashlib.sha256(str(candidate).encode()).hexdigest()
            if hash_result[: len(PROOF_OF_WORK_PREFIX)] == PROOF_OF_WORK_PREFIX:
                return new_proof
            new_proof += 1

    def hash(self, block: BlockDTO) -> str:
        """Return the SHA-256 hash of *block* (excluding block_hash to avoid circularity)."""
        raw = {
            "index": block.index,
            "timestamp": block.timestamp.isoformat(),
            "proof": block.proof,
            "previous_hash": block.previous_hash,
        }
        encoded = json.dumps(raw, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()

    def get_full_chain(self) -> list[BlockDTO]:
        rows = self._crud.get_data(
            fields=self._fields,
            table=BLOCKCHAIN_TABLE,
            get_amount=100_000,
            extra='ORDER BY "index" ASC',
        )
        return [BlockDTO(**row) for row in rows]

    def chain_valid(self, chain: list[BlockDTO]) -> bool:
        for i in range(1, len(chain)):
            current = chain[i]
            previous = chain[i - 1]

            if current.previous_hash != self.hash(previous):
                return False

            candidate = current.proof ** 2 - previous.proof ** 2
            hash_result = hashlib.sha256(str(candidate).encode()).hexdigest()
            if hash_result[: len(PROOF_OF_WORK_PREFIX)] != PROOF_OF_WORK_PREFIX:
                return False

        return True

    def mine_block(self) -> BlockDTO:
        """Convenience: find proof and append next block."""
        previous_block = self.get_last_block()
        proof = self.proof_of_work(previous_block.proof)
        previous_hash = self.hash(previous_block)
        return self.create_block(proof, previous_hash)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _create_genesis_block(self) -> None:
        existing = self._crud.get_data(
            fields=self._fields,
            table=BLOCKCHAIN_TABLE,
            get_amount=1,
        )
        if not existing:
            self.create_block(proof=1, previous_hash="0")