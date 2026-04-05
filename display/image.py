try:
    from mlx import *
except ImportError as e:
    raise SystemExit(f"Unable to import mlx: {e}")
import numpy as np

class Image():
    def __init__(self, mlx: Mlx, mlx_ptr, width: int, height: int):
        self.width = width
        self.height = height

        self.ptr = mlx.mlx_new_image(mlx_ptr, width, height)
        data, bpp, line_size, fmt = mlx.mlx_get_data_addr(self.ptr)
        self.data = np.ctypeslib.as_array(data, np.uint8)
        self.data = self.data.reshape(height, line_size)
        self.bpp = bpp
        self.line_size = line_size
        self.fmt = fmt

        self.colors = {}
