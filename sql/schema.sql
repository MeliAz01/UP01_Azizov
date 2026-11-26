-- Таблицы создаются ORM-моделями SQLAlchemy при запуске сервера.
-- Этот файл содержит только контрольный запрос структуры:
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN ('books', 'readers', 'book_loans')
ORDER BY table_name;
