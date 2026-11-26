from datetime import date
from sqlalchemy import (
    String, Integer, SmallInteger, Date, ForeignKey, CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class Book(Base):
    __tablename__ = "books"
    __table_args__ = (
        CheckConstraint("total_copies >= 0"),
        CheckConstraint("available_copies >= 0"),
        CheckConstraint("available_copies <= total_copies"),
    )
    book_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    author: Mapped[str] = mapped_column(String(150), nullable=False)
    genre: Mapped[str] = mapped_column(String(100), nullable=False)
    publication_year: Mapped[int | None] = mapped_column(SmallInteger)
    publisher: Mapped[str | None] = mapped_column(String(150))
    isbn: Mapped[str | None] = mapped_column(String(20), unique=True)
    total_copies: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    available_copies: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    loans: Mapped[list["BookLoan"]] = relationship(back_populates="book")

class Reader(Base):
    __tablename__ = "readers"
    reader_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    middle_name: Mapped[str | None] = mapped_column(String(60))
    phone: Mapped[str | None] = mapped_column(String(20))
    email: Mapped[str | None] = mapped_column(String(120))
    card_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    registration_date: Mapped[date] = mapped_column(Date, nullable=False)
    loans: Mapped[list["BookLoan"]] = relationship(back_populates="reader")

class BookLoan(Base):
    __tablename__ = "book_loans"
    __table_args__ = (
        CheckConstraint("due_date >= loan_date"),
        CheckConstraint("return_date IS NULL OR return_date >= loan_date"),
        CheckConstraint("status IN ('Активна', 'Возвращена', 'Просрочена')"),
    )
    loan_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.book_id"), nullable=False)
    reader_id: Mapped[int] = mapped_column(ForeignKey("readers.reader_id"), nullable=False)
    loan_date: Mapped[date] = mapped_column(Date, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    return_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Активна")
    book: Mapped[Book] = relationship(back_populates="loans")
    reader: Mapped[Reader] = relationship(back_populates="loans")
