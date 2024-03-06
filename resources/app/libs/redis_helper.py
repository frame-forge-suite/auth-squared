import ast
from typing import Any

from app.config import settings
from redis import Redis as RedisBase

from .logger import Logger


def get(key: str) -> Any | None:
    """
    Get a value from Redis.

    Args:
        key (str): Key to get the value for.

    Returns:
        Any | None: Value for the given key or None if not found.
    """
    log = Logger.get_logger(__name__)
    try:
        redis_client: RedisBase = RedisBase.from_url(settings.redis.url)
        value = redis_client.get(key)
        redis_client.close()
        if isinstance(value, bytes):
            if "token" in key or not value.decode("utf-8").startswith(("{", "[")):
                return value.decode("utf-8")
            value = ast.literal_eval(value.decode("utf-8"))

        # log.info("Redis get : " + key + " : " + str(value))
        return value
    except Exception as e:
        log.error(f"Redis get error : {e}")
        return None


def set(key: str, value: Any, expiration: int | None = None) -> None:
    """
    Set a value in Redis.

    Args:
        key (str): Key to set the value for.
        value (Any): Value to set.
        expiration (int, optional): Expiration time in seconds. Defaults to None.
    """

    log = Logger.get_logger(__name__)
    try:
        # Convert value to bytes if it is not a bytes, string, int or float
        if not isinstance(value, (bytes, str, int, float)):
            value = str(value).encode("utf-8")
        redis_client: RedisBase = RedisBase.from_url(settings.redis.url)
        redis_client.set(key, value, ex=expiration)
        redis_client.close()
        # log.info(
        #     f"Redis set : {key}" + f" with expiration {expiration}"
        #     if expiration
        #     else ""
        # )
    except Exception as e:
        log.error(f"Redis set error : {e}")


def delete(key: str) -> None:
    """
    Delete a value from Redis.

    Args:
        key (str): Key to delete the value for.
    """
    log = Logger.get_logger(__name__)
    try:
        redis_client: RedisBase = RedisBase.from_url(settings.redis.url)
        redis_client.delete(key)
        redis_client.close()
        # log.info("Redis delete : " + key)
    except Exception as e:
        log.error(f"Redis delete error : {e}")
