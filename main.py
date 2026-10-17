from __future__ import annotations

import time
import uuid
from typing import Callable

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response

EMAIL = "23f3003450@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-58vl6u.example.com"

app = FastAPI(title="Dynamic Stats API", version="1.0.0")

# Only this exact origin receives Access-Control-Allow-Origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
    max_age=600,
)


@app.middleware("http")
async def request_metadata(request: Request, call_next: Callable):
    """Add request ID and elapsed-time headers to ordinary and preflight responses."""
    started = time.perf_counter()
    request_id = str(uuid.uuid4())
    try:
        response: Response = await call_next(request)
    except Exception:
        # Keep the required metadata headers even if an unexpected server-side
        # exception occurs in downstream application code.
        response = JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

    elapsed = max(0.0, time.perf_counter() - started)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{elapsed:.6f}"
    return response


@app.get("/")
def root():
    return {"service": "Dynamic Stats API", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/stats")
def stats(values: str = Query(..., description="Comma-separated integers")):
    raw_items = values.split(",")
    if not raw_items or any(item.strip() == "" for item in raw_items):
        raise HTTPException(status_code=400, detail="values must be a comma-separated list of integers")

    try:
        numbers = [int(item.strip()) for item in raw_items]
    except ValueError:
        raise HTTPException(status_code=400, detail="values must be a comma-separated list of integers")

    if not numbers:
        raise HTTPException(status_code=400, detail="at least one integer is required")

    total = sum(numbers)
    return {
        "email": EMAIL,
        "count": len(numbers),
        "sum": total,
        "min": min(numbers),
        "max": max(numbers),
        "mean": total / len(numbers),
    }
