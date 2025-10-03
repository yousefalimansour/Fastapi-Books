from sqlmodel import create_engine ,text
from  sqlalchemy.ext.asyncio import AsyncEngine
from src.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True, future=True)
async_engine = AsyncEngine(engine)


async def init_db():
    async with async_engine.begin() as conn:
        from src.books.model import Book  
        await conn.run_sync(Book.metadata.create_all)
