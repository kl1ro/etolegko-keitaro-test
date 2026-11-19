# Keitaro campaign manager

A test assignment: a campaign creator and an offer editor on top of the Keitaro Admin API.

- `backend/` — FastAPI, SQLAlchemy, Alembic (Python 3.13, uv)
- `frontend/` — Next.js
- `docker-compose.yml` — Postgres, the API and the web app

## Run

1. Create `.env` from the example and fill in `KEITARO_API_KEY` (the key is in the Keitaro admin panel):

   ```sh
   cp .env.example .env
   ```

2. Start everything:

   ```sh
   docker compose up --build
   ```

   - web app: http://localhost:3000
   - API docs: http://localhost:8000/docs

Before the API starts, the one-shot `migrate` service applies pending migrations (`alembic upgrade head`) and exits; the API waits for it to finish successfully. Migrations therefore run once per start, not once per API container.

## Migrations

Apply migrations by hand:

```sh
docker compose run --rm migrate alembic upgrade head
```

Create a migration after changing models in `backend/app/models.py` (the database must be running; `alembic/versions` is mounted, so the file lands in the repository):

```sh
docker compose run --rm migrate alembic revision --autogenerate -m "describe the change"
```

Roll back the last migration:

```sh
docker compose run --rm migrate alembic downgrade -1
```

## Local development without Docker

Postgres from compose is exposed on `localhost:5432`, so the API can run on the host against it:

```sh
docker compose up -d db

cd backend
uv sync
set -a; . ../.env; set +a
export DATABASE_URL=postgresql+psycopg://keitaro:keitaro@localhost:5432/keitaro
uv run alembic upgrade head
uv run uvicorn app.main:app --reload

cd ../frontend
npm install
npm run dev
```
