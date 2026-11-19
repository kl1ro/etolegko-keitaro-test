set -e

socat TCP-LISTEN:5555,fork,reuseaddr TCP:127.0.0.1:5556 &

exec prisma studio \
  --url "postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}" \
  --port 5556 \
  --browser none
