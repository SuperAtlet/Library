from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from typing import Annotated
from fastapi import Depends

DATABASE_URL = "sqlite+aiosqlite:///library.db"

engine = create_async_engine(DATABASE_URL)
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase, MappedAsDataclass):
    pass

async def get_db():
    async with new_session() as session:
        yield session

# Аннотация для удобного использования в эндпоинтах
SessionDep = Annotated[AsyncSession, Depends(get_db)]