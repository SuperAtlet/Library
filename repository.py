from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.books import BooksModel
from schemas.books import SBookAdd


class BookRepository:
    @classmethod
    async def add_one(cls, data: SBookAdd, session: AsyncSession) -> BooksModel:
        # 1. Превращаем данные из Pydantic в словарь
        books_dict = data.model_dump()

        # 2. Создаем объект модели
        book = BooksModel(**books_dict)

        # 3. Добавляем и сохраняем
        session.add(book)
        await session.commit()
        await session.refresh(book)

        # 4. Возвращаем созданный объект
        return book

    @classmethod
    async def find_all(cls, session: AsyncSession) ->list[BooksModel]:
        # 1. Готовим запрос
        query = select(BooksModel)

        # 2. Выполняем
        result = await session.execute(query)

        # 3. Возвращаем список объектов
        books_models = result.scalars().all()
        return books_models
    @classmethod
    async def find_by_id(cls,session: AsyncSession,book_id:int) ->BooksModel | None:
        return await session.get(BooksModel,book_id)
    @classmethod
    async def update(cls,session: AsyncSession,book_id:int,data:SBookAdd) ->BooksModel | None:
        book = await cls.find_by_id(session,book_id)
        if not book:
            return None
        for key,value in data.model_dump().items():
            setattr(book,key,value)
        await session.commit()
        await session.refresh(book)
        return book
    @classmethod
    async def delete(cls,session: AsyncSession,book_id:int) -> bool:
        book = await cls.find_by_id(session,book_id)
        if not book:
            return False
        await session.delete(book)
        await session.commit()
        return True


