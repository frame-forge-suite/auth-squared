from __future__ import annotations

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.openapi.utils import get_openapi

from app.config.settings import settings
from app.routers.api import system_utils
from app.routers import root

app = FastAPI()

# ? Create main API Router
api_router = APIRouter(prefix="/api/v1")

# ? Include routers
api_router.include_router(system_utils.router)

# ? Include main API Router in the app
app.include_router(api_router)
app.include_router(root.router)


# ? OpenAPI docs
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.openapi.title,
        version=settings.openapi.version,
        summary=settings.openapi.summary,
        description=settings.openapi.description,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": settings.openapi.logo_url,
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.server.reload,
        log_level=settings.server.log_level,
        log_config=settings.server.log_config,
    )
