from .image import Image
from constants import *
try:
    import cv2
except ImportError as e:
    raise SystemExit(f"Unable to import cv2: {e}")

def rotate_image(image: Image, angle: float) -> None:
    img = image.data.reshape(image.height, image.width, image.bytes_pp)
    center = (image.width // 2, image.height // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, scale=(1 / 1.414) * MAZE_SCALE)
    rotated = cv2.warpAffine(img, matrix, (image.width, image.height))
    image.data[:image.height, :image.width * (image.bytes_pp)] = rotated.reshape(image.height, image.width * (image.bytes_pp))
