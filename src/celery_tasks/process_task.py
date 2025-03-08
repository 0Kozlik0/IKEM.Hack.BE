from celery import Celery

from config import get_settings
from model.predict import process_npy_images
from process_cells.geojson_convertor import from_npy_to_geojson
from process_cells.patch_manager import cut_image_to_patches, merge_patches
from tifffile import imread
import os


celery_app = Celery(
    "my_app",
    broker="redis://ikem_redis:6379/0",
    backend="redis://ikem_redis:6379/0",
)


@celery_app.task(name="celery_tasks.process_task.predict_patch_task")
def predict_patch_task(details: dict):

    print(details)

    # Save Image
    # image_path = details["image_name"]
    image_path = "test.ome.tif"
    
    
    # Load TIFF file from tiff_store folder
    print("Loading TIFF file ...")
    tiff_store_path = os.path.join('../tiff_store', image_path)
    image = imread(tiff_store_path)

    print("TIFF file loaded")

    # Create ROI
    print("Creating ROI ...")
    # x = details["x"]
    # y = details["y"]
    # width = details["width"]
    # height = details["height"]

    x = 100
    y = 100
    width = 256
    height = 256

    image = image[y:y+height, x:x+width]
    print("ROI created")

    # Create patches
    print("Creating patches ...")
    parameters = {
        "x": x,
        "y": y,
        "width": width,
        "height": height
    } # Check if this is correct
    patches = cut_image_to_patches(image=image,
                                   parameters=parameters,
                                   patch_size=256)
    print("Patches created")
    # Predict patches
    print("Predicting patches ...")
    predicted_masks = process_npy_images(patches=patches)
    print("Patches predicted")

    # Create merged mask
    merged_mask = merge_patches(predicted_masks=predicted_masks,
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

    return {
        "geojson": geojson,
        "statistics": []
    }
