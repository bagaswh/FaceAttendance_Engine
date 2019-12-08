import base64
import cv2
import numpy as np


def get_rgb_small_frame(image):
    small_frame = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = image[:, :, ::-1]
    return rgb_small_frame


def b64decode(base64str):
    '''
      Decode base64-encoded OpenCV image back to OpenCV image.
    '''
    decoded = base64.b64decode(base64str)
    nparr = np.frombuffer(decoded, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image


def b64encode(image):
    '''
      Encode OpenCV image to base64 string.
    '''
    image_encoded = cv2.imencode('.jpg', image)
    encoded = base64.b64encode(image_encoded)
    return encoded
