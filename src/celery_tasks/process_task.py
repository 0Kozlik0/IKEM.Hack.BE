from celery import Celery

from config import get_settings


celery_app = Celery(
    "my_app",
    broker="redis://ikem_redis:6379/0",
    backend="redis://ikem_redis:6379/0",
)


@celery_app.task(name="celery_tasks.process_task.predict_patch")
def predict_patch(details: dict):

    print(details)
    
    # Save Image

    # Create ROI

    # Create patches
    patches = cut_image_to_patches(image=image,
                                   parameters=parameters,
                                   patch_size=256)
    
    # Predict patches

    # Create Geojson

    # Create Statistics

    return {
        "geojson": geojson,
        "statistics": statistics
    }
