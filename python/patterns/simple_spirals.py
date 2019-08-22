from .base_pattern import BasePattern
from .utils import n_pixels, n_strips, create_palette, pick_color


class SimpleSpirals(BasePattern):
    name = 'Simple Spirals'

    def __init__(self):
        self.tick = 0
        self.palette = create_palette(n_pixels)

    def render(self, pixels):
        self.tick += 1
        for s in range(n_strips):
            p = pixels[s]
            p[int(17 * s + self.tick) % 150] = pick_color(self.palette, s * 27 + self.tick)
            for i in range(n_pixels):
                p[i].scale_luminance(-0.05)
                p[i].clip_black(0.07)
