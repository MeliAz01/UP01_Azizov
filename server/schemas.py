from datetime import date
from pydantic import BaseModel, ConfigDict, Field

class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=150)
    genre: str = Field(min_length=1, max_length=100)
    publication_year: int | None = None
    publisher: str | None = None
    isbn: str | None = None
    total_copies: int = Field(default=1, ge=0)
    available_copies: int = Field(default=1, ge=0)

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class BookOut(BookBase):
    book_id: int
    model_config = ConfigDict(from_attributes=True)

class ReaderBase(BaseModel):
    last_name: str
    first_name: str
    middle_name: str | None = None
    phone: str | None = None
    email: str | None = None
    card_number: str
    registration_date: date

class ReaderCreate(ReaderBase):
    pass

class ReaderUpdate(ReaderBase):
    pass

class ReaderOut(ReaderBase):
    reader_id: int
    model_config = ConfigDict(from_attributes=True)

class LoanCreate(BaseModel):
    book_id: int
    reader_id: int
    loan_date: date
    due_date: date

class LoanOut(BaseModel):
    loan_id: int
    book_id: int
    reader_id: int
    loan_date: date
    due_date: date
    return_date: date | None
    status: str
    model_config = ConfigDict(from_attributes=True)
