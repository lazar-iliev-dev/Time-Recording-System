FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# System dependencies (only what is necessary)
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc libpq-dev ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

# Upgrade pip & install Python deps without cache
RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

# Note: using main:app because main.py is located in backend/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
