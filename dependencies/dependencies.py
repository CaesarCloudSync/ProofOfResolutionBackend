"""FastAPI dependency providers."""

from __future__ import annotations

from functools import lru_cache

from fastapi import Depends

from BlockChain.BlockChain import BlockChain
from CaesarJWT.CaesarJWT import CaesarJWT
from CaesarSQLDB.CaesarCRUD import CaesarCRUD
from CaesarSQLDB.CaesarCreateTables import CaesarCreateTables
from repositories.ResolutionRepository import ResolutionRepository
from services.ResolutionService import ResolutionService


@lru_cache(maxsize=1)
def get_crud() -> CaesarCRUD:
    return CaesarCRUD()


@lru_cache(maxsize=1)
def get_create_tables() -> CaesarCreateTables:
    return CaesarCreateTables()


@lru_cache(maxsize=1)
def get_blockchain() -> BlockChain:
    crud = get_crud()
    create_tables = get_create_tables()
    create_tables.create(crud)          # idempotent – CREATE TABLE IF NOT EXISTS
    return BlockChain(crud, create_tables)


@lru_cache(maxsize=1)
def get_jwt_service() -> CaesarJWT:
    return CaesarJWT(get_crud())


def get_resolution_service(
    blockchain: BlockChain = Depends(get_blockchain),
    crud: CaesarCRUD = Depends(get_crud),
    create_tables: CaesarCreateTables = Depends(get_create_tables),
) -> ResolutionService:
    repository = ResolutionRepository(crud, create_tables)
    return ResolutionService(blockchain, repository)