FROM python:3.11-slim

WORKDIR /code

COPY . .

# Install necessary build tools and dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements_docker.txt

CMD ["python", "-u", "-m", "server.server", "--host", "0.0.0.0", "--port", "4444", "--reload"]