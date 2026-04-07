import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import Literal


class Uvicorn(BaseModel):
    host: str = os.getenv("HOST", "127.0.0.1")
    port: str = os.getenv("PORT", 8000)


class Gunicorn(Uvicorn):
    workers: int = 4
    timeout: int = 900


class Logging(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    access_log_format: str = (
        '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
    )


class RunSettings(BaseModel):
    uvicorn: Uvicorn = Uvicorn()
    gunicorn: Gunicorn = Gunicorn()
    logging: Logging = Logging()


settings = RunSettings()
