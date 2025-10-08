FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/* \
	&& pip install --no-cache-dir -r requirements.txt
COPY . /app
ENV PYTHONUNBUFFERED=1
CMD ["python", "-u", "edge_sim.py"]