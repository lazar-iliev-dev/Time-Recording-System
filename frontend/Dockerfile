FROM node:18-alpine
WORKDIR /app
COPY package*.json ./

# fallback to npm install if package-lock.json missing
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

COPY . .

ENV PORT=3000
EXPOSE 3000

CMD ["npm", "run", "dev"]