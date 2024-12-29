# Use the official Python slim image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the bot script and requirements file to the container
COPY bot.py /app/bot.py
COPY requirements.txt /app/requirements.txt

# Install system dependencies (if needed) and Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Expose the port the bot will run on
EXPOSE 8080

# Set environment variables to prevent Python from generating .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Run the bot script when the container starts
CMD ["python", "test.py"]
