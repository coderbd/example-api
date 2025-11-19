from datetime import datetime, timezone

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI(title="Example API", version="0.1.0")


class Greeting(BaseModel):
    message: str
    audience: str
    generated_at: datetime


@app.get("/", response_model=Greeting, tags=["greetings"], summary="Return a friendly greeting")
def read_root(name: str = Query(default="World", min_length=1, max_length=50)) -> Greeting:
    """Return a simple greeting that includes the provided name."""
    now = datetime.now(timezone.utc)
    return Greeting(message=f"Hello, {name}!", audience=name, generated_at=now)


@app.get("/health", tags=["system"], summary="Liveness check")
def healthcheck() -> dict[str, str]:
    """Expose a lightweight liveness endpoint for container orchestration probes."""
    return {"status": "ok"}
