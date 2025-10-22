FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# System packages: minimal + postgresql client for pg_isready
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc libpq-dev postgresql-client ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r /app/requirements.txt

# copy app code
COPY . /app

# ensure entrypoint and wait script are executable
RUN chmod +x /app/entrypoint.sh /app/wait-for-postgres.sh || true

EXPOSE 8000

# use non-root? optional; for simplicity we run as root in dev image
# user creation omitted for dev; add for prod hardened image

CMD ["/app/entrypoint.sh"]
