# Менеджер кампаний Keitaro

Тестовое задание: создание кампаний и редактор офферов поверх Keitaro Admin API.

- `backend/` — FastAPI, SQLAlchemy, Alembic (Python 3.13, uv)
- `frontend/` — Next.js
- `docker-compose.yml` — Postgres, API и веб-приложение

## Запуск

1. Создайте `.env` из примера и заполните `KEITARO_API_KEY` (ключ есть в админке Keitaro):

   ```sh
   cp .env.example .env
   ```

2. Соберите образы:

   ```sh
   docker compose build
   ```

3. Запустите базу данных и примените миграции:

   ```sh
   docker compose up -d db
   docker compose run --rm migrate
   ```

4. Запустите всё:

   ```sh
   docker compose up
   ```

   - веб-приложение: http://localhost:3000
   - документация API: http://localhost:8000/docs

`docker compose up` никогда не запускает миграции: сервис `migrate` спрятан за профилем `migrate`, поэтому стартует, только если назвать его явно. На серверах его запускает этап migrate в CI перед деплоем; локально запускайте его вручную после того, как подтянули новые миграции.

## Миграции

Применить миграции:

```sh
docker compose run --rm migrate
```

Создать миграцию после изменения моделей в `backend/app/models.py` (база данных должна быть запущена; `alembic/versions` примонтирована, поэтому файл появится в репозитории):

```sh
docker compose run --rm migrate alembic revision --autogenerate -m "describe the change"
```

Откатить последнюю миграцию:

```sh
docker compose run --rm migrate alembic downgrade -1
```

## Просмотр базы данных

Prisma Studio запускается отдельным сервисом `studio`. Он читает базу напрямую по её URL, поэтому ему не нужна схема Prisma, и он работает рядом с SQLAlchemy:

```sh
docker compose up --build studio
```

Затем откройте http://localhost:5555. Сервис спрятан за профилем `studio`, поэтому `docker compose up` его не запускает, а его порт открыт только на localhost.
