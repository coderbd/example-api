# syntax=docker/dockerfile:1.6
FROM python:3.12-slim AS base

ARG ENV_SECRET

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/app/.venv

# Put the virtualenv's `bin` dir onto PATH so runtime tools installed by
# `uv sync` are available without explicit activation (sourcing) in later
# layers or at container start.
ENV PATH=$UV_PROJECT_ENVIRONMENT/bin:$PATH

ENV ENV_SECRET ${ENV_SECRET}

WORKDIR /app

# Install uv for deterministic dependency management
RUN pip install --no-cache-dir --upgrade pip uv

# Pre-copy dependency files to leverage Docker layer caching
COPY pyproject.toml uv.lock ./

# Install only the runtime dependencies defined in the lockfile
RUN uv sync --frozen --no-dev

# Copy the FastAPI source code
COPY api ./api
COPY README.md ./

EXPOSE 8000

# Run Uvicorn and use 4 worker processes for modest production concurrency.
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
