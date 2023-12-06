FROM python:3.11-slim

WORKDIR /code

COPY . .
RUN pip install --no-cache-dir -r requirements_docker.txt


CMD ["python", "-u", "-m", "server.server", "--host", "0.0.0.0", "--port", "4444", "--reload"]