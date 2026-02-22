# seed.py
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from database import new_session
from repository import BookRepository
from schemas.books import SBookAdd

async def seed_data():
    # Создаём сессию вручную
    async with new_session() as session:
        # Список книг для добавления
        books_data = [
            {"title": "Война и мир", "author": "Лев Толстой", "year": 1869, "pages": 1300, "is_read": False},
            {"title": "Преступление и наказание", "author": "Фёдор Достоевский", "year": 1866, "pages": 800, "is_read": False},
            {"title": "Мастер и Маргарита", "author": "Михаил Булгаков", "year": 1967, "pages": 480, "is_read": True},
        ]

        for book_dict in books_data:
            # Превращаем словарь в схему Pydantic
            book_schema = SBookAdd(**book_dict)
            # Добавляем книгу через репозиторий
            await BookRepository.add_one(book_schema, session)
            print(f"Добавлена книга: {book_dict['title']}")

if __name__ == "__main__":
    asyncio.run(seed_data())