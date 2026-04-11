try:
    from mlx import Mlx
except ImportError as e:
    raise SystemExit(f"Unable to import mlx: {e}")
from display import Image, Font
from constants import BLACK, WHITE, RED, GREEN #noqa

def handle_key_press(keycode, params):
    mlx, mlx_ptr = params
    if keycode == 0xFF1B or keycode == ord('q'):
        mlx.mlx_loop_exit(mlx_ptr)

def handle_close(params):
    mlx, mlx_ptr = params
    mlx.mlx_loop_exit(mlx_ptr)

if __name__ == '__main__':
    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    window_width = 500
    window_height = 500
    win_ptr = mlx.mlx_new_window(mlx_ptr, window_width, window_height, "A-maze-ing")
    image = Image(mlx, mlx_ptr, window_width+1, window_height+1)
    image.set_to(WHITE)
    font = Font('display/DeterminationMono')
    font.print(image, 10, 10, 'Hello world!', color=BLACK, bg_color=GREEN)
    mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, image.ptr, 0, 0)

    mlx.mlx_hook(win_ptr, 33, 0, handle_close, (mlx, mlx_ptr))
    mlx.mlx_hook(win_ptr, 2, 1, handle_key_press, (mlx, mlx_ptr))
    mlx.mlx_loop(mlx_ptr)

    mlx.mlx_destroy_image(mlx_ptr, image.ptr)
    mlx.mlx_destroy_window(mlx_ptr, win_ptr)
    mlx.mlx_release(mlx_ptr)
