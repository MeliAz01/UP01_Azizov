# uvicorn server.main:app --reload
from fastapi import FastAPI
from .database import Base, engine
from .routers import books, readers, loans

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Электронный каталог библиотеки",
    description="REST API для учёта книг, читателей и выдач",
    version="1.0.0"
)
app.include_router(books.router)
app.include_router(readers.router)
app.include_router(loans.router)

@app.get("/")
def root():
    return {"message": "API электронного каталога библиотеки", "docs": "/docs"}
