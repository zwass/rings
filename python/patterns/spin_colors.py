from math import sin, cos

from .base_pattern import BasePattern
from .utils import n_pixels, n_strips, create_palette, pick_color, rotate_array


class SpinColors(BasePattern):
    name = 'Spin Colors'

    def __init__(self):
        self.tick = 0
        self.palette = create_palette(n_pixels)

    def render(self, pixels):
        self.tick += 1
        t = self.tick / 10

        for s in range(n_strips):
            for i in range(n_pixels):
                # pixels[i] = create_color((i + t*37 + (17*s)))
                # pixels[i] = create_color(
                #     i +
                #     t * 37 +
                #     t_factor * cos(t) * sin(t) +
                #     (17*s) +
                #     t_factor * -15 * cos(s + t/13)
                # )
                pixels[s][i] = pick_color(self.palette, (3*i + 23*cos(t)*sin(t)) - (150*cos(3.3*s + t/13)) + 47*t)
                # pixels[i].scale_luminance(-.3 * sin(s/n_strips*pi))
                # pixels[i] = create_color(((37*sin(i) +
                # 23*cos(t)*sin(t)) - (150*cos(s + t/13)) + 47*t))
            pixels[s] = rotate_array(pixels[s], int(30 * sin(s*7 + t)))
