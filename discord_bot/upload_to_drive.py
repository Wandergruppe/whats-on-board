import logging
import os
from firebase_admin import credentials, storage, initialize_app

cred = credentials.Certificate("firebase.json")
initialize_app(cred, {'storageBucket': 'STORAGE BUCKET URL HERE'})


def upload_pics_to_bucket() -> bool:
    # Put your local file path
    files = os.listdir("image")
    logging.info(f"Found {len(files)} files. Uploading...")
    bucket = storage.bucket()
    for folder in files:
        for picture in os.listdir(f"image/{folder}"):
            blob = bucket.blob(folder + "/" + picture)
            try:
                blob.upload_from_filename(f"image/{folder}/{picture}")
            except:
                logging.error("Upload Failed")
                return False
    return True


def delete_images_from_directory() -> None:
    files = os.listdir("image")
    logging.info(f"Found {len(files)} files. Deleting...")
    for folder in files:
        for picture in os.listdir(f"image/{folder}"):
            os.remove(f"image/{folder}/{picture}")


def upload_and_delete() -> bool:
    success = upload_pics_to_bucket()
    if success:
        delete_images_from_directory()
        return True
    else:
        return False
