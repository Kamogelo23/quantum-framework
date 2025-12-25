# Multi-stage Docker build for ML Service with Ollama

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including curl for Ollama
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create models directory
RUN mkdir -p models

# Expose ports (8001 for FastAPI, 11434 for Ollama)
EXPOSE 8001 11434

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=90s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8001/health')"

# Create startup script
RUN echo '#!/bin/bash\n\
# Start Ollama server in background\n\
ollama serve &\n\
OLLAMA_PID=$!\n\
\n\
# Wait for Ollama to be ready\n\
echo "Waiting for Ollama to start..."\n\
sleep 5\n\
\n\
# Pull Qwen 2.5 14B model (only if not already present)\n\
if ! ollama list | grep -q "qwen2.5:14b"; then\n\
    echo "Pulling Qwen 2.5 14B model (this may take 5-10 minutes on first run)..."\n\
    ollama pull qwen2.5:14b\n\
    echo "Model downloaded successfully!"\n\
else\n\
    echo "Qwen 2.5 14B model already present"\n\
fi\n\
\n\
# Start FastAPI service\n\
echo "Starting ML Service..."\n\
python serving/model_server.py\n\
' > /app/start.sh && chmod +x /app/start.sh

# Run startup script
CMD ["/app/start.sh"]
