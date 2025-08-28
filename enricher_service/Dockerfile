# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy enricher service code
COPY enricher_service/ ./enricher_service/

# Copy common folder (publisher & consumer)
COPY common/ ./common/

# Install dependencies
COPY enricher_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download nltk data
RUN python -m nltk.downloader vader_lexicon stopwords

# Set environment variables (optional)
ENV KAFKA_BROKERS=broker:9092

# Run main.py by default
CMD ["python", "enricher_service/app/main.py"]
