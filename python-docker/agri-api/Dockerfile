FROM python:3.13-slim

WORKDIR /app

# System dependencies (safe + helps if wheels are missing)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

#create the directly to match the local folder staructure
RUN mkdir -p /app/agri_api

# Copy dependency manifests first (for Docker layer caching)
COPY pyproject.toml uv.lock /app/

# Install dependencies exactly as locked
RUN uv sync --frozen

# Copy application code
COPY . /app/agri_api/

# This is just the metadata the main exposure of port should happen in the docker compose 
EXPOSE 8000

RUN chmod +x /app/agri_api/entrypoint.sh

CMD ["/app/agri_api/entrypoint.sh"]
