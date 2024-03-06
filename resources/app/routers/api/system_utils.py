from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/system-utils",
    tags=["System Utils"],
)

@router.get("/healthcheck", summary="Health Check", description="Health Check for the API")
def health_check():
    return JSONResponse(status_code=200, content={"status": "up"})