from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    """Server settings used to configure the Uvicorn server."""

    model_config = SettingsConfigDict(case_sensitive=False, env_prefix="SERVER_")

    host: str = "0.0.0.0"
    port: int = 80
    reload: bool = False
    log_level: str = "info"
    log_config: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "format": "%(asctime)s - [%(levelname)s] [%(threadName)s] %(name)s::%(funcName)s %(message)s (%(filename)s:%(lineno)d)",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "use_colors": True,
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "format": "%(asctime)s - [%(levelname)s] [%(threadName)s] %(name)s::%(funcName)s %(message)s (%(filename)s:%(lineno)d)",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "use_colors": True,
            },
        },
        "filters": {"healthcheck_filter": {"()": "app.libs.logger.HealthCheckFilter"}},
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "filters": ["healthcheck_filter"],
            },
        },
        "loggers": {
            "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
            "uvicorn.error": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["access"],
                "level": "INFO",
                "propagate": False,
            },
        },
        "root": {"handlers": ["default"], "level": "DEBUG", "propagate": False},
    }


class PostgreSQLSettings(BaseSettings):
    """PostgreSQL settings used to connect to the database."""

    model_config = SettingsConfigDict(case_sensitive=False, env_prefix="SQL_")

    url: str


class RedisSettings(BaseSettings):
    """Redis settings used to connect to the Redis instance."""

    model_config = SettingsConfigDict(case_sensitive=False, env_prefix="REDIS_")

    url: str


class OpenAPISettings(BaseSettings):
    """OpenAPI settings used to generate the OpenAPI schema."""

    title: str = "FFS - AuthSquared API"
    version: str = "v1"
    summary: str = "FFS - AuthSquared API - OpenAPI schema"
    description: str = (
        "This is the OpenAPI schema for the FFS - AuthSquared API. This API is used to manage the authentication and authorization of the FFS platform."
    )
    logo_url: str = (
        "https://avatars.githubusercontent.com/u/161715938?s=400&u=d0035e79c26570a7c4cf3ff721b2d323a558aab0&v=4"
    )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False)

    server: ServerSettings = ServerSettings()
    openapi: OpenAPISettings = OpenAPISettings()
    postgresql: PostgreSQLSettings = PostgreSQLSettings()
    redis: RedisSettings = RedisSettings()


# ? Settings instance to be used in the application
settings = Settings()
