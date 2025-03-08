from celery import Celery

from config import get_settings
from model.predict import process_npy_images
from process_cells.geojson_convertor import from_npy_to_geojson
from process_cells.patch_manager import cut_image_to_patches, merge_patches
from tifffile import TiffFile, imread
import os

import subprocess
import numpy as np

celery_app = Celery(
    "my_app",
    broker="redis://ikem_redis:6379/0",
    backend="redis://ikem_redis:6379/0",
    broker_connection_retry_on_startup=True,
)

celery_app.conf.worker_max_memory_per_child = None  # No memory limit per worker
celery_app.conf.worker_max_tasks_per_child = 1  # Restart worker after each task to free memory
celery_app.conf.task_soft_time_limit = 3600  # 1 hour soft time limit
celery_app.conf.task_time_limit = 3600 * 2  # 2 hour hard time limit


@celery_app.task(name="celery_tasks.process_task.predict_patch_task")
def predict_patch_task(details: dict):

    print(details)

    # Save Image
    # image_path = details["image_name"]
    image_path = "test.ome.tif"

    # Load TIFF file from tiff_store folder
    print("Loading TIFF file ...")
    tiff_store_path = os.path.join('../tiff_store', image_path)
    
    # Try a smaller region from a different part of the image
    y = 10000  # Try different coordinates
    x = 58000
    width = 256  # Smaller region for testing
    height = 256
    
    # Create a temporary output file
    temp_output = "/tmp/region_extract.tif"
    
    # Use gdal_translate to extract just the region (requires GDAL to be installed)
    cmd = [
        "gdal_translate", 
        "-srcwin", str(x), str(y), str(width), str(height),
        tiff_store_path, 
        temp_output
    ]
    subprocess.run(cmd, check=True)
    
    # Now load the much smaller extracted region
    image = imread(temp_output)
    
    # Clean up
    # os.remove(temp_output)

    print("Image shape: ", image.shape)

    print("TIFF file loaded")

    # Create ROI
    # print("Creating ROI ...")
    # x = details["x"]
    # y = details["y"]
    # width = details["width"]
    # height = details["height"]

    # image = image[y:y+height, x:x+width]
    # print("ROI created")

    # Create patches
    print("Creating patches ...")
    parameters = [x, y, width, height]
    patches = cut_image_to_patches(image=image,
                                   parameters=parameters,
                                   patch_size=256)
    print("Patches created")
    # Predict patches
    print("Predicting patches ...")
    predicted_masks = process_npy_images(npy_images=patches)
    predicted_masks = np.array(predicted_masks)
    print("Patches predicted")

    # Create merged mask
    merged_mask = merge_patches(masks=predicted_masks,
                                original_size=(image.shape[0], image.shape[1]),
                                patch_size=256)
    
    print("Merged mask created")
    # Create Geojson
    print("Creating Geojson ...")
    geojson = from_npy_to_geojson(merged_mask)
    print("Geojson created")

    # Create threshold postprocessing
    # geojson = threshold_postprocessing(geojson)

    # Create Statistics
    # statistics = create_statistics(patches=patches, predicted_masks=predicted_masks)


    # Convert GeoDataFrame to a serializable format
    if hasattr(geojson, 'to_json'):
        geojson = geojson.to_json()
        
    return {
        "geojson": geojson,
        "statistics": []
    }
