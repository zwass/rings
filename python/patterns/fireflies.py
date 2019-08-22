from math import fabs, sin

from .base_pattern import BasePattern
from .utils import n_pixels, n_strips, create_palette, pick_color


class Fireflies(BasePattern):
    name = 'Fireflies'

    def __init__(self):
        self.tick = 0
        self.palette = create_palette(n_pixels)

    def render(self, pixels):
        self.tick += 1
        for s in range(n_strips):
            p = pixels[s]
            idx = int(150 * fabs(sin(3 * s + self.tick)))
            p[idx] = pick_color(self.palette, s * 17 + self.tick)
            for i in range(n_pixels):
                p[i].scale_luminance(-0.07)
