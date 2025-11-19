import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel


load_dotenv()

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


@app.get(
    "/secret",
    tags=["system"],
    summary="Expose configured ENV_SECRET",
    responses={404: {"description": "Secret not configured"}},
)
def read_secret() -> dict[str, str]:
    """Return the configured ENV_SECRET to help validate deployment wiring."""
    secret = os.getenv("ENV_SECRET")
    if not secret:
        raise HTTPException(status_code=404, detail="ENV_SECRET is not configured")
    return {"secret": secret}
