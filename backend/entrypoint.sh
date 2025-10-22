#!/usr/bin/env sh
set -e

# location of helper
WAIT_SCRIPT="/app/wait-for-postgres.sh"

# If wait script exists, use it; otherwise simple sleep fallback
if [ -x "$WAIT_SCRIPT" ]; then
  echo "[entrypoint] Waiting for Postgres..."
  # pass DATABASE_URL if needed or default host/port
  /app/wait-for-postgres.sh "${DATABASE_URL:-postgresql://user:password@db:5432/mydatabase}"
else
  echo "[entrypoint] wait script not found, sleeping 5s"
  sleep 5
fi

# Run migrations (alembic must be available in image)
echo "[entrypoint] Running alembic migrations..."
alembic upgrade head

# Start the web server
echo "[entrypoint] Starting uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000

cp backend/entrypoint.sh backend/entrypoint.sh.bak
sed -i '' 's/exec uvicorn main:app/exec uvicorn app.main:app/' backend/entrypoint.sh

grep -n "uvicorn" backend/entrypoint.sh || true
cat backend/entrypoint.sh
