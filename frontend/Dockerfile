FROM node:20-bullseye-slim

WORKDIR /app

COPY package*.json ./

RUN npm ci --no-audit --no-fund

COPY . .

ENV PORT=3000
EXPOSE 3000

CMD ["npm", "run", "dev"]
