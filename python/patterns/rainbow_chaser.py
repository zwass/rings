from math import fabs, sin, cos, pi

from .base_pattern import BasePattern
from .utils import Color, n_pixels, n_strips, rotate_array, clear_pixels


class RainbowChaser(BasePattern):
    name = 'Rainbow Chaser'

    def __init__(self):
        self.tick = 0

    def render(self, pixels):
        clear_pixels(pixels)
        self.tick += 1
        for s in range(n_strips):
            s_pct = float(s + 1) / (n_strips + 1)
            base_hue = (s_pct + self.tick / 37) % 1.0
            p = pixels[s]
            lum_pct = cos(float((s + self.tick) % n_strips) / n_strips * pi) * .5 + .2
            lum_pct = .5
            for i in range(int(sin((s + 1) / n_pixels * self.tick) * 150)):
                i_pct = (float(i - self.tick) % n_pixels) / n_pixels
                hue = (base_hue + 0.33 * (0.5 - sin(i_pct*pi))) % 1.0
                sat = fabs(sin((i_pct + s_pct) * pi))
                p[i] = Color(hue=hue, luminance=lum_pct, saturation=sat)
            pixels[s] = rotate_array(p, int((s * 7 + self.tick * 3) * (-1 if (s % 2) else 1) + self.tick))
