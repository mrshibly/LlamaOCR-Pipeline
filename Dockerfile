# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Bypass PaddleOCR connectivity check
ENV DISABLE_MODEL_SOURCE_CHECK=True

# Install system dependencies for OpenCV and PaddleOCR
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    cmake \
    python3-dev \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 7860 (Hugging Face default)
EXPOSE 7860

# Command to run the application
CMD ["python", "app.py"]
