FROM node:22-alpine

RUN apk add --no-cache socat && npm install --global prisma@7.10.1

COPY start.sh /start.sh

EXPOSE 5555

CMD ["sh", "/start.sh"]
