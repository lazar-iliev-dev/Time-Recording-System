#!/usr/bin/env sh
# Usage: wait-for-postgres.sh <DATABASE_URL>
# Simple utility that retries connecting to Postgres until success or timeout.
# Expects psql to be available in the image (we'll install it via apt in Dockerfile)
set -e

DATABASE_URL="$1"
# parse host and port from URL crudely (postgresql://user:pass@host:port/dbname)
# fallback values:
HOST="db"
PORT="5432"
RETRIES=30
SLEEP=2

# attempt naive parse
if echo "$DATABASE_URL" | grep -q "@"; then
  # extract host:port after @
  HOSTPORT=$(echo "$DATABASE_URL" | sed -E 's#.*@([^/]*).*#\1#')
  HOST=$(echo "$HOSTPORT" | cut -d: -f1)
  PORT=$(echo "$HOSTPORT" | cut -s -d: -f2 || echo "$PORT")
fi

i=0
while [ $i -lt $RETRIES ]; do
  if pg_isready -h "$HOST" -p "$PORT" >/dev/null 2>&1; then
    echo "[wait-for-postgres] Postgres is available at $HOST:$PORT"
    exit 0
  fi
  i=$((i+1))
  echo "[wait-for-postgres] waiting for postgres... ($i/$RETRIES)"
  sleep $SLEEP
done

echo "[wait-for-postgres] timeout waiting for Postgres at $HOST:$PORT"
exit 1
