FROM node:22-alpine

RUN apk add --no-cache socat && npm install --global prisma@7.10.1

EXPOSE 5555

CMD socat TCP-LISTEN:5555,bind=$(hostname -i),fork,reuseaddr TCP:127.0.0.1:5555 & \
  exec prisma studio \
    --url "postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}" \
    --port 5555 \
    --browser none
