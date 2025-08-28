# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy service code
COPY ./app ./app
COPY ./requirements.txt ./requirements.txt
COPY ./.env ./.env

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable to point to env file (optional if loaded in code)
ENV DOTENV_PATH=./.env

# Run the main.py file
CMD ["python", "app/main.py"]
