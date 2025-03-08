from multiprocessing.pool import AsyncResult
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from celery_tasks.process_task import predict_patch_task

router = APIRouter()

@router.get("/test")
async def test():
    return {"message": "Hello, World!"}

@router.post("/predict_patch")
async def predict_patch(details: dict):

    result = predict_patch_task.delay(details)

    return JSONResponse(
            content={
                "message": "Processing tiff file started",
                "task_id": result.id,
            },
            status_code=200,
        )

@router.get("/predict_patch/{task_id}")
async def predict_patch(task_id: str):
    result = AsyncResult(task_id)
    return JSONResponse(
        content={"result": result.result},
        status_code=200,
    )


@router.get("/get_status/{task_id}")
async def get_status(task_id: str):
    result = AsyncResult(task_id)
    return JSONResponse(
        content={"status": result.status},
        status_code=200,
    )

@router.post("/predict_wholeslide")
async def predict_patch(details: dict):
    return {"message": "Hello, World!"}
