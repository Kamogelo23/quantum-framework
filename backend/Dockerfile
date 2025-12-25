# Multi-stage Docker build for Python FastAPI Backend

# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt
# Multi-stage Docker build for Python FastAPI Backend

# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies and Tectonic LaTeX compiler
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Tectonic for LaTeX compilation
RUN wget https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.15.0/tectonic-0.15.0-x86_64-unknown-linux-musl.tar.gz \
    && tar -xzf tectonic-0.15.0-x86_64-unknown-linux-musl.tar.gz \
    && mv tectonic /usr/local/bin/ \
    && chmod +x /usr/local/bin/tectonic \
    && rm tectonic-0.15.0-x86_64-unknown-linux-musl.tar.gz

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 quantum && \
    chown -R quantum:quantum /app

USER quantum

# Expose port
EXPOSE 8000

# Run Django with gunicorn and uvicorn workers (for async/WebSocket support)
CMD ["gunicorn", "quantum.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "--workers", "4"]
