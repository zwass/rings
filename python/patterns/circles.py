from math import pi, sin, fabs

from .base_pattern import BasePattern
from .utils import Color, n_pixels, n_strips


class Circles(BasePattern):
    name = 'Circles'

    def __init__(self):
        self.tick = 0

    def render(self, pixels):
        self.tick += 1
        t = self.tick / 10
        for s in range(n_strips):
            for i in range(n_pixels):
                r_idx = (i + 7*s + 13*t) / n_pixels * pi * 2
                g_idx = (i + 5*s - 7*t) / n_pixels * pi * 2 + (pi / 2)
                b_idx = (i + 13*s + 9*t) / n_pixels * pi * 2 + (pi)
                pixels[s][i] = Color(
                    rgb=(fabs(sin(r_idx)), fabs(sin(g_idx)), fabs(sin(b_idx)))
                )
                # color = color_utils.contrast(color, 128, sin(((s / n_strips) + t / 2) * pi * 2))
