from sqlmodel import Field, SQLModel ,Column
from sqlalchemy.dialects import postgresql as pg
import uuid
from datetime import datetime



class Book(SQLModel, table=True):
    __tablename__ = "books"

    Uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            unique=True,
            nullable=False,
            index=True,
        )
)
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    created_at: datetime = Field(Column(pg.TIMESTAMP(timezone=True), default=datetime.now))
    updated_at: datetime = Field(Column(pg.TIMESTAMP(timezone=True), default=datetime.now, onupdate=datetime.now))


    def __repr__(self):
        return f"Book(title={self.title}, author={self.author}, publisher={self.publisher})"


        