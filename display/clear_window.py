try:
    from mlx import *
except ImportError as e:
    raise SystemExit(f"Unable to import mlx: {e}")
from .image import Image
from .color import endian_color
from constants import *
import numpy as np
from ctypes import c_void_p

def clear_window(mlx: Mlx, mlx_ptr: c_void_p, win_ptr: c_void_p, image: Image):
    color = 0xFF_00_00_00 if image.fmt == 0 else 0x00_00_00_FF
    image.data.view(np.uint32)[:] = color
    mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, image.ptr, 0, 0)
