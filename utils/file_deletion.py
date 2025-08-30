from loguru import logger
import os


def clear_dir(dir_path: str):
    if os.path.isdir(dir_path):
        logger.info(f"Clearing directory '{dir_path}'...")
        for file_name in os.listdir(dir_path):
            delete_file(file_path=os.path.join(dir_path, file_name))
    else:
        logger.info(f"'{dir_path}' is not a directory.")


def delete_file(file_path: str):
    if os.path.isfile(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            logger.error(f"Could not remove {file_path}: {e}")
