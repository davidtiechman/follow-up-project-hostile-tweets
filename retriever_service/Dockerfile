# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install netcat-openbsd for wait-for-it
RUN apt-get update \
    && apt-get install -y netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of the app
COPY . .

# Make wait-for-it.sh executable
RUN chmod +x /app/wait-for-it.sh

# Start the service after waiting for Kafka
CMD ["kafka:9092", "--timeout=60", "--strict", "--", "python", "app/main.py"]
