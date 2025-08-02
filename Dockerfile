# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install system dependencies for newspaper3k
RUN apt-get update && apt-get install -y \
    build-essential libxml2-dev libxslt-dev libjpeg-dev zlib1g-dev libcurl4-openssl-dev python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Download nltk punkt data
RUN python -m nltk.downloader punkt

# Expose the port
EXPOSE 5000

# Start the app
CMD ["python", "app.py"]
