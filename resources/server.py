from __future__ import annotations

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.config.settings import settings

app = FastAPI()


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
