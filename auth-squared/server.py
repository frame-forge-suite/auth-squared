from __future__ import annotations

import uvicorn
from os import getenv
from fastapi import FastAPI

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=80, reload=bool(getenv("SERVER_RELOAD", False)))