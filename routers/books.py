from fastapi import APIRouter,HTTPException, status
from sqlalchemy.orm import Session

from database import SessionDep
from schemas.books import SBook, SBookAdd
from repository import BookRepository  # Импортируем наш новый класс

router = APIRouter(prefix="/books", tags=["Книги"])

@router.post("", response_model=SBook,status_code=status.HTTP_201_CREATED)
async def create_book(book: SBookAdd,session: SessionDep):
    # Вся логика сохранения ушла в репозиторий.
    # Роутер просто передает данные и ждет результат.
    book_model = await BookRepository.add_one(book, session)
    return book_model

@router.get("/{book_id}", response_model=list[SBook],status_code=status.HTTP_200_OK)
async def get_books(session: SessionDep,):
    books = await BookRepository.find_all(session)
    return books

@router.get("/{book_id}",response_model=SBook)
async def get_book(book_id:int, session: SessionDep,):
    book = await BookRepository.find_by_id(session,book_id)
    if not book:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Книга не найдена'
    )
    return book
@router.put("/{book_id}",response_model=SBook)
async def update_book(book_id:int,book_data: SBookAdd,session: SessionDep):
    book = await BookRepository.update(session,book_id,book_data)
    if not book:
        raise HTTPException(status_code=404)
    return book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, session: SessionDep):
    deleted = await BookRepository.delete(session, book_id)
    if not deleted:
        raise HTTPException(status_code=404)
    # Не возвращаем ничего – FastAPI автоматически сформирует пустой ответ с кодом 204

