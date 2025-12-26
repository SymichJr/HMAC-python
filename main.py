"""Main module for run FastAPI application"""

import uvicorn

from src.app import app
from src.core.config import get_config

if __name__ == '__main__':
    cfg = get_config()
    listen = cfg.listen.split(":")
    host = listen[0]
    port = listen[1]
    uvicorn.run(app, host=host, port=int(port))
