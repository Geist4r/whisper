# Dockerfile for Whisper API on Railway
FROM python:3.11-slim

# Install system dependencies (FFmpeg is required for Whisper)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire whisper package
COPY whisper/ ./whisper/
COPY api.py .
COPY pyproject.toml .
COPY README.md .
COPY LICENSE .
COPY MANIFEST.in .

# Install whisper package in editable mode
RUN pip install -e .

# Expose port (Railway will set PORT env variable)
EXPOSE 8000

# Run the API server
CMD ["python", "api.py"]
