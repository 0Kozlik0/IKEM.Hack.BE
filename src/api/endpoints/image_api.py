from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
import os
import uuid
import shutil
from typing import List, Optional

router = APIRouter()

# Define the base directory for storing images
TIFF_STORE_DIR = "/tiff_store"

@router.get("/list")
async def list_images(folder: Optional[str] = None):
    """List all available images in the tiff store or a specific folder"""
    target_dir = TIFF_STORE_DIR
    
    if folder:
        target_dir = os.path.join(TIFF_STORE_DIR, folder)
    
    if not os.path.exists(target_dir):
        raise HTTPException(status_code=404, detail=f"Folder {folder} not found")
    
    files = []
    for root, _, filenames in os.walk(target_dir):
        rel_path = os.path.relpath(root, TIFF_STORE_DIR)
        for filename in filenames:
            if any(filename.lower().endswith(ext) for ext in ['.tif', '.tiff', '.png', '.jpg', '.jpeg']):
                file_path = os.path.join(rel_path, filename)
                if rel_path == '.':
                    file_path = filename
                files.append({
                    "name": filename,
                    "path": file_path,
                    "url": f"/static/{file_path}"
                })
    
    return {"images": files}

@router.post("/upload")
async def upload_image(file: UploadFile = File(...), folder: Optional[str] = None):
    """Upload an image to the tiff store"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Validate file type
    if not any(file.filename.lower().endswith(ext) for ext in ['.tif', '.tiff', '.png', '.jpg', '.jpeg']):
        raise HTTPException(status_code=400, detail="File must be an image (tif, png, jpg)")
    
    # Create target directory if it doesn't exist
    target_dir = TIFF_STORE_DIR
    if folder:
        target_dir = os.path.join(TIFF_STORE_DIR, folder)
        os.makedirs(target_dir, exist_ok=True)
    
    # Generate unique filename to prevent overwrites
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(target_dir, unique_filename)
    
    # Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Generate the URL for accessing the file
    relative_path = os.path.relpath(file_path, TIFF_STORE_DIR)
    url = f"/static/{relative_path}"
    
    return {
        "filename": unique_filename,
        "original_filename": file.filename,
        "path": relative_path,
        "url": url
    }

@router.get("/view/{path:path}")
async def get_image(path: str):
    """Get a specific image by path"""
    file_path = os.path.join(TIFF_STORE_DIR, path)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(file_path)

@router.get("/download/{path:path}")
async def download_image(path: str):
    """Download a specific image by path"""
    file_path = os.path.join(TIFF_STORE_DIR, path)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(
        file_path,
        media_type='application/octet-stream',
        filename=os.path.basename(path)
    )