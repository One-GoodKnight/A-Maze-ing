from .image import Image
import numpy as np

def endian_color(image: Image, argb: int):
    if (not argb in image.colors):
            if image.fmt == 1:
                image.colors[argb] = np.array([
                    argb >> 24 & 0xFF, argb >> 16 & 0xFF,
                    argb >> 8 & 0xFF, argb & 0xFF],
                dtype=np.uint8)
            else:
                image.colors[argb] = np.array([
                    argb & 0xFF, argb >> 8 & 0xFF,
                    argb >> 16 & 0xFF, argb >> 24 & 0xFF],
                dtype=np.uint8)
    return image.colors[argb]
