FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y --no-install-recommends gcc libpq-dev ca-certificates \
 && rm -rf /var/lib/apt/lists/* \
 && pip install --no-cache-dir -r requirements.txt

COPY . /app
ENV PYTHONUNBUFFERED=1
EXPOSE 9000

CMD ["uvicorn", "edge_sim:app", "--host", "0.0.0.0", "--port", "9000", "--reload"]
