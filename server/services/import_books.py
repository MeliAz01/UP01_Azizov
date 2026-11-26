from openpyxl import load_workbook
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import Book

EXPECTED_HEADERS = [
    "title", "author", "genre", "publication_year",
    "publisher", "isbn", "total_copies", "available_copies"
]

def import_books_xlsx(file_path: str, db: Session) -> dict:
    wb = load_workbook(file_path, read_only=True, data_only=True)
    ws = wb.active
    headers = [str(c).strip() if c is not None else "" for c in next(ws.iter_rows(values_only=True))]
    if headers[:len(EXPECTED_HEADERS)] != EXPECTED_HEADERS:
        wb.close()
        raise ValueError("Неверные заголовки XLSX. Ожидаются: " + ", ".join(EXPECTED_HEADERS))

    added, errors = 0, []
    for row_no, values in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        if not values or all(v is None for v in values):
            continue
        try:
            values = list(values) + [None] * (8 - len(values))
            title, author, genre, year, publisher, isbn, total, available = values[:8]
            if not title or not author or not genre:
                raise ValueError("Не заполнено название, автор или жанр")
            total = int(total if total is not None else 1)
            available = int(available if available is not None else total)
            if total < 0 or available < 0 or available > total:
                raise ValueError("Некорректное количество экземпляров")
            if isbn and db.scalar(select(Book).where(Book.isbn == str(isbn))):
                raise ValueError("ISBN уже существует")
            db.add(Book(
                title=str(title), author=str(author), genre=str(genre),
                publication_year=int(year) if year is not None else None,
                publisher=str(publisher) if publisher else None,
                isbn=str(isbn) if isbn else None,
                total_copies=total, available_copies=available
            ))
            db.flush()
            added += 1
        except Exception as exc:
            db.rollback()
            errors.append(f"Строка {row_no}: {exc}")
    db.commit()
    wb.close()
    return {"added": added, "errors": errors}
