from .base_pattern import BasePattern
from .utils import Color, n_pixels, n_strips, clear_pixels


class Helix(BasePattern):
    name = 'Helix'

    def __init__(self):
        self.tick = 0

    def render(self, pixels):
        clear_pixels(pixels)
        self.tick += 1
        t = self.tick / 10
        for s in range(n_strips):
            index = int(t * 7 + s*13) % n_pixels
            pixels[s][index] = Color(hsl=((index % n_pixels) / 150, 1.0, .5))
            pixels[s][(index + 50) % n_pixels] = Color(hsl=(((index + 50) % n_pixels) / 150, 1.0, .5))
            pixels[s][(index + 100) % n_pixels] = Color(hsl=(((index + 100) % n_pixels) / 150, 1.0, .5))
