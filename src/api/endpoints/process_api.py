from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
async def test():
    return {"message": "Hello, World!"}

@router.post("/predict_patch")
async def predict_patch(details: dict):
    return {"message": "Hello, World!"}

@router.post("/predict_wholeslide")
async def predict_patch(details: dict):
    return {"message": "Hello, World!"}
