from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Reader
from ..schemas import ReaderCreate, ReaderUpdate, ReaderOut

router = APIRouter(prefix="/api/readers", tags=["Читатели"])

@router.get("/", response_model=list[ReaderOut])
def list_readers(db: Session = Depends(get_db)):
    return db.scalars(select(Reader).order_by(Reader.last_name, Reader.first_name)).all()

@router.get("/{reader_id}", response_model=ReaderOut)
def get_reader(reader_id: int, db: Session = Depends(get_db)):
    reader = db.get(Reader, reader_id)
    if not reader:
        raise HTTPException(404, "Читатель не найден")
    return reader

@router.post("/", response_model=ReaderOut, status_code=201)
def create_reader(data: ReaderCreate, db: Session = Depends(get_db)):
    reader = Reader(**data.model_dump())
    db.add(reader)
    db.commit()
    db.refresh(reader)
    return reader

@router.put("/{reader_id}", response_model=ReaderOut)
def update_reader(reader_id: int, data: ReaderUpdate, db: Session = Depends(get_db)):
    reader = db.get(Reader, reader_id)
    if not reader:
        raise HTTPException(404, "Читатель не найден")
    for key, value in data.model_dump().items():
        setattr(reader, key, value)
    db.commit()
    db.refresh(reader)
    return reader

@router.delete("/{reader_id}", status_code=204)
def delete_reader(reader_id: int, db: Session = Depends(get_db)):
    reader = db.get(Reader, reader_id)
    if not reader:
        raise HTTPException(404, "Читатель не найден")
    if reader.loans:
        raise HTTPException(409, "Нельзя удалить читателя с историей выдач")
    db.delete(reader)
    db.commit()
    return Response(status_code=204)
