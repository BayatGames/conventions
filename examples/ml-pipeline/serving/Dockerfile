FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for logs and model registry
RUN mkdir -p logs model_registry

# Expose ports for API and Prometheus metrics
EXPOSE 8080 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV MODEL_CONFIG_PATH=/app/config/model_serving_config.json

# Run the API server
CMD ["python", "api/model_api.py"]