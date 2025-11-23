# Example API

Sample FastAPI project targeting Python 3.12 and managed entirely with [uv](https://docs.astral.sh/uv/). It exposes a greeting endpoint plus a lightweight health probe and includes pytest-based regression tests.

## Requirements

- Python 3.12 (installable via `uv python install 3.12`)
- `uv` 0.9+ on your PATH

## Quickstart

```bash
# optional: ensure the requested interpreter is available
uv python install 3.12

# install dependencies declared in pyproject.toml / uv.lock
uv sync --python 3.12

# run the FastAPI dev server (auto-reload, live docs)
uv run fastapi dev api.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

## Running with Docker

```bash
# build the image (optionally pass a secret build-arg)
docker build -t example-api .

# run the container, reading runtime environment from a local `.env` file
docker run --rm -p 8000:8000 --env-file .env example-api
```

Notes:
- The image places the application's virtual environment at `/app/.venv` and
	adds its `bin/` directory to `PATH`, so runtime tools installed by `uv sync`
	(including `uvicorn`) are available automatically in the container.
- The container starts Uvicorn with `--workers 4` by default to provide modest
	concurrency for production-like runs. To override the worker count, run the
	server yourself inside the container or modify the `CMD` in the `Dockerfile`.

## Running tests

```bash
uv run pytest
```

## Project layout

```
example_api/
├── api/
│   ├── __init__.py
│   └── main.py          # FastAPI application with greeting + health routes
├── tests/
│   ├── __init__.py
│   └── test_root.py     # pytest coverage for the public endpoints
├── pyproject.toml       # project metadata + dependencies managed by uv
└── uv.lock              # locked dependency graph for Python 3.12
```

## API overview

- `GET /` — Responds with a structured greeting payload (`Greeting` schema) and accepts an optional `name` query parameter.
- `GET /health` — Lightweight liveness probe returning `{ "status": "ok" }`.

Both endpoints are documented automatically via FastAPI's OpenAPI schema.

## Managing dependencies with uv

- Add a runtime dependency: `uv add <package>`
- Add a dev-only dependency: `uv add --dev <package>`
- Remove obsolete packages: `uv remove <package>`
- Refresh the lockfile for Python 3.12: `uv lock --python 3.12`

After updating dependencies, rerun `uv sync` to apply the new lockfile. Commit both `pyproject.toml` and `uv.lock` so collaborators stay in sync.

## Deploying

For a production-style process manager (gunicorn, systemd, container, etc.) run Uvicorn directly via uv:

```bash
uv run uvicorn api.main:app --host 0.0.0.0 --port 8000
```

The service is stateless, so it is ready to be containerized or deployed on any ASGI-compatible hosting provider.
