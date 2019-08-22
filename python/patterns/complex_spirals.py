from math import fabs, sin

from .base_pattern import BasePattern
from .utils import n_pixels, n_strips, create_palette, pick_color


class ComplexSpirals(BasePattern):
    name = 'Complex Spirals'

    def __init__(self):
        self.tick = 0
        self.palette = create_palette(n_pixels)

    def render(self, pixels):
        self.tick += 1
        for s in range(n_strips):
            splay = 53 * sin(self.tick/53)
            p = pixels[s]
            p[int(splay * (s+1) + self.tick) % 150] = pick_color(
                self.palette, s * 27 + self.tick
            )
            for i in range(n_pixels):
                p[i].scale_luminance(-0.07)
