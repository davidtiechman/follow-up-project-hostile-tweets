# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the code into the container
COPY cleaning ./cleaning


# Copy any other necessary files if needed
# COPY .env .   # optional, only if you want to include env inside container

# Set environment variables (optional, can also be in docker-compose)
# ENV PYTHONUNBUFFERED=1

# Default command to run your processor service
CMD ["python", "cleaning/app/main.py"]
