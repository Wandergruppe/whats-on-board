import datetime
import os.path
import logging
import cv2
import numpy as np


class Camera:

    def __init__(self, camera_id: int, windows: bool, width: int, height: int) -> None:
        self.camera_id = camera_id
        self.exposure = 0
        self.auto_exposure = True
        self.width = width
        self.height = height
        self.windows = windows

    def init_camera(self) -> None:
        if self.windows:
            self.picture = cv2.VideoCapture(self.camera_id, cv2.CAP_DSHOW)
        else:
            self.picture = cv2.VideoCapture(self.camera_id)
        self.picture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.picture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        if self.auto_exposure:
            self.picture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
        else:
            self.picture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
            self.picture.set(cv2.CAP_PROP_EXPOSURE, self.exposure)

    def get_current_board(self, channel: str, colour: bool) -> str:
        self.init_camera()
        _, frame = self.picture.read()
        if not colour:
            frame = image_editing(frame)
        date = str(datetime.datetime.now()).replace(":", "-").replace(".", "-")
        if not os.path.exists(f"image/{channel}"):
            logging.warn("Image folder does not exist")
            os.makedirs(f"image/{channel}")
        path = f'image/{channel}/{date}.png'.replace(" ", "_")
        cv2.imwrite(path, frame)
        self.picture.release()
        return path

    def calculate_exposure(self) -> None:
        logging.info("Getting auto exposure")
        cam = self.picture
        # Set to manual exposure
        cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        # Capture an image with low exposure
        cam.set(cv2.CAT_PROP_EXPOSURE, -5)
        _, low_exp = cam.read()
        # Capture an image with high exposure
        cam.set(cv2.CAP_PROP_EXPOSURE, 5)
        _, high_exp = cam.read()
        # Calculate the difference between the two images
        diff = cv2.absdiff(low_exp, high_exp)
        # Calculate the average difference
        avg = np.mean(diff)
        # Calculate the exposure compensation as integer and set it
        exposure_compensation = int(np.log2(avg / 12.92) * 12)
        cam.set(cv2.CAP_PROP_EXPOSURE, exposure_compensation)

    def change_exposure(self, ec: int, auto: bool) -> None:
        if auto:
            self.auto_exposure = True
        else:
            self.auto_exposure = False
            self.exposure = ec


def correct_perspective_distortion(frame, original_points, new_points):
    """
    Correct the perspective distortion given an image and points
    """
    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(original_points, new_points)
    return cv2.warpPerspective(frame, matrix, (frame.shape[1], frame.shape[0]))


def transform_frame(frame) -> (np.array, np.array):
    # TODO: We need some way to find the points of an image
    pts1 = np.float32([[125, 100], [1175, 105],
                       [130, 870], [1160, 870]])
    pts2 = np.float32([[0, 0], [1280, 0],
                       [0, 720], [1280, 720]])
    return correct_perspective_distortion(frame, pts1, pts2)


def image_editing(image):
    """
    This function will edit the image to make it easier to read using adaptive thresholding
    """
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Blur the image to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # Dilate the image to make the text thicker
    return thresh
