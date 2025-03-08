"""
This module contains the Setting class with all app configurations.
"""

import os
from functools import lru_cache
import torch

from dotenv import load_dotenv


@lru_cache()
def get_settings():
    """
    Return the cached settings object.
    """
    return Settings()


class Settings:
    """
    This class contains all configuration loaded from environment files.
    """

    load_dotenv(".env")

    deploy = os.environ.get("DEPLOY")

    # FOLDERS
    iedl_root_dir = os.environ.get("IEDL_ROOT_DIR")
    reload = os.environ.get("RELOAD")

    app_name = os.environ.get("APP_NAME")
    log_level = os.environ.get("LOG_LEVEL")

    # uvicorn setup
    port = int(str(os.environ.get("UVICORN_PORT")))
    host = os.environ.get("UVICORN_HOST")
    workers = int(str(os.environ.get("UVICORN_WORKERS")))
