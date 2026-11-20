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

2. Pull the images CI built from `main` (if the packages are private, log in first: `docker login ghcr.io` with a token that has `read:packages`):

   ```sh
   docker compose pull
   ```

3. Start the database and apply migrations:

   ```sh
   docker compose up -d db
   docker compose run --rm migrate
   ```

4. Start everything:

   ```sh
   docker compose up
   ```

   - web app: http://localhost:3000
   - API docs: http://localhost:8000/docs

`docker compose up` never runs migrations: the `migrate` service sits behind the `migrate` profile, so it starts only when named explicitly. On servers the CI migrate stage runs it before deploying; locally run it by hand after pulling new migrations.

### Build the images locally

The app services have both an image and a build context, and Compose pulls by default. To build from source instead:

```sh
docker compose up -d --build
```

Local builds get the same image names as the pulled ones, so plain `docker compose up` keeps using them. To get the CI images back:

```sh
docker compose up -d --pull always
```

## Migrations

Apply migrations:

```sh
docker compose run --rm migrate
```

Create a migration after changing models in `backend/app/models.py` (the database must be running; `alembic/versions` is mounted, so the file lands in the repository):

```sh
docker compose run --rm migrate alembic revision --autogenerate -m "describe the change"
```

Roll back the last migration:

```sh
docker compose run --rm migrate alembic downgrade -1
```

## Browsing the database

Prisma Studio runs as a separate `studio` service. It reads the database directly from its URL, so it needs no Prisma schema and works next to SQLAlchemy:

```sh
docker compose up studio
```

Then open http://localhost:5555. The service sits behind the `studio` profile, so `docker compose up` never starts it, and its port is bound to localhost only.

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
