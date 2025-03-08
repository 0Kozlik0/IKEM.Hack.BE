from fastapi import APIRouter

from .endpoints import process_api, image_api

api_router = APIRouter()

api_router.include_router(process_api.router, tags=["Data processing API"])
api_router.include_router(image_api.router, prefix="/images", tags=["Image API"])