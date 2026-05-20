"""FastAPI dependency providers."""

from __future__ import annotations

from functools import lru_cache

from fastapi import Depends

from BlockChain.BlockChain import BlockChain
from Security.JWTService import JWTService
from Database.CRUD import CRUD
from Database.CreateTables import CreateTables
from repositories.ResolutionRepository import ResolutionRepository
from services.ResolutionService import ResolutionService


@lru_cache(maxsize=1)
def get_crud() -> CRUD:
    return CRUD()


@lru_cache(maxsize=1)
def get_create_tables() -> CreateTables:
    return CreateTables()


@lru_cache(maxsize=1)
def get_blockchain() -> BlockChain:
    crud = get_crud()
    create_tables = get_create_tables()
    create_tables.create(crud)          # idempotent – CREATE TABLE IF NOT EXISTS
    return BlockChain(crud, create_tables)


@lru_cache(maxsize=1)
def get_jwt_service() -> JWTService:
    return JWTService(get_crud())


def get_resolution_service(
    blockchain: BlockChain = Depends(get_blockchain),
    crud: CRUD = Depends(get_crud),
    create_tables: CreateTables = Depends(get_create_tables),
) -> ResolutionService:
    repository = ResolutionRepository(crud, create_tables)
    return ResolutionService(blockchain, repository)