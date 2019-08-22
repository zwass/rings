from .base_pattern import BasePattern
from .utils import Color, n_pixels, n_strips


class RainbowSpirals(BasePattern):
    name = 'Rainbow Spirals'

    def __init__(self):
        self.tick = 0

    def render(self, pixels):
        self.tick += 1
        t = self.tick / 10
        for s in range(n_strips):
            for i in range(n_pixels):
                pixels[s][i] = Color(hsl=(((i + t*37 + 17*s) % n_pixels) / n_pixels, 1.0, .5))
