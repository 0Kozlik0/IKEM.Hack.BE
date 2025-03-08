import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import torch
import logging


from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware


from api.api import api_router
from config import get_settings

settings = get_settings()

# on startup check if iedl_root_dir exist

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

app = FastAPI(middleware=middleware)

# Mount static files directory for serving images
app.mount("/static", StaticFiles(directory="/tiff_store"), name="static")

app.include_router(api_router, prefix="/ikem_api")

def main():
    """
    Run the backend app using uvicorn.
    """
    uvicorn.run(
        "app:app",
        reload=settings.reload,
        host=settings.host,
        port=settings.port,
        workers=settings.workers,
    )


if __name__ == "__main__":
    main()