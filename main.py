from fastapi import FastAPI
from routers import books as book_router
from database import engine, Model
from models.books import BooksModel  # явный импорт модели
app = FastAPI(title="Library")

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:

        await conn.run_sync(Model.metadata.create_all)

app.include_router(book_router.router)


