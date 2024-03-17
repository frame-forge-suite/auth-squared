from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(tags=["System Utils"])


@router.get("/", summary="Root", description="Root Route")
def root():
    return JSONResponse(
        status_code=200,
        content={"status": "up", "message": "AuthSquared API is up and running"},
    )
