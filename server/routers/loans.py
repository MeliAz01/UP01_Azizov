from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Book, Reader, BookLoan
from ..schemas import LoanCreate, LoanOut

router = APIRouter(prefix="/api/book-loans", tags=["Выдачи"])

@router.get("/", response_model=list[LoanOut])
def list_loans(status: str | None = None, db: Session = Depends(get_db)):
    stmt = select(BookLoan).order_by(BookLoan.loan_date.desc())
    if status:
        stmt = stmt.where(BookLoan.status == status)
    return db.scalars(stmt).all()

@router.post("/", response_model=LoanOut, status_code=201)
def create_loan(data: LoanCreate, db: Session = Depends(get_db)):
    if data.due_date < data.loan_date:
        raise HTTPException(422, "Срок возврата не может быть раньше даты выдачи")
    try:
        book = db.scalar(
            select(Book).where(Book.book_id == data.book_id).with_for_update()
        )
        reader = db.get(Reader, data.reader_id)
        if book is None:
            raise HTTPException(404, "Книга не найдена")
        if reader is None:
            raise HTTPException(404, "Читатель не найден")
        if book.available_copies < 1:
            raise HTTPException(409, "Нет доступных экземпляров")
        book.available_copies -= 1
        loan = BookLoan(**data.model_dump(), status="Активна")
        db.add(loan)
        db.commit()
        db.refresh(loan)
        return loan
    except Exception:
        db.rollback()
        raise

@router.put("/{loan_id}/return", response_model=LoanOut)
def return_loan(loan_id: int, db: Session = Depends(get_db)):
    try:
        loan = db.scalar(
            select(BookLoan).where(BookLoan.loan_id == loan_id).with_for_update()
        )
        if loan is None:
            raise HTTPException(404, "Операция выдачи не найдена")
        if loan.status == "Возвращена":
            raise HTTPException(409, "Книга уже возвращена")
        book = db.scalar(
            select(Book).where(Book.book_id == loan.book_id).with_for_update()
        )
        loan.return_date = date.today()
        loan.status = "Возвращена"
        book.available_copies += 1
        db.commit()
        db.refresh(loan)
        return loan
    except Exception:
        db.rollback()
        raise
