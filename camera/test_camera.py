from time import sleep

import cv2

from camera.camera import *


def test_transform_frame():
    frame = transform_frame(cv2.imread('../image/whiteboard.jpg'))
    cv2.imwrite('transform_image.jpg', frame)


def test_image_editing():
    img = image_editing(cv2.imread('../image/whiteboard.jpg'))
    cv2.imwrite('image_editing.jpg', img)


def test_both():
    img = transform_frame(cv2.imread('../image/whiteboard.jpg'))
    # Crop to 1280x720
    img = img[0:720, 0:1280]
    img = image_editing(img)
    cv2.imwrite('both.jpg', img)
