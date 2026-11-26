# Электронный каталог библиотеки

## Требования
- Python 3.10+
- PostgreSQL 14+

## Установка
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

Создайте базу данных PostgreSQL с именем `library`. Скопируйте `.env.example` в `.env` и задайте `DATABASE_URL` с корректным логином и паролем.

## Запуск
Из корневой папки проекта:
```bash
uvicorn server.main:app --reload
```
Документация API: http://127.0.0.1:8000/docs

## Основные маршруты
- `GET/POST /api/books/`
- `GET/PUT/DELETE /api/books/{book_id}`
- `GET/POST /api/readers/`
- `GET/PUT/DELETE /api/readers/{reader_id}`
- `GET/POST /api/book-loans/`
- `PUT /api/book-loans/{loan_id}/return`

Для поиска книг используйте параметры `title`, `author`, `genre`.
