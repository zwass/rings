from math import sin, pi

from .base_pattern import BasePattern
from .utils import Color, n_strips, n_pixels


def distance(i):
    d = 74 - i
    if d < 0:
        d = -1 * d - 1
    return d


class Center(BasePattern):
    name = 'Center Waves'

    def __init__(self):
        self.tick = 0.0

    def render(self, pixels):
        for s in range(n_strips):
            hue = (s + self.tick/10) % n_strips / n_strips
            for i in range(n_pixels):
                target = int(0.5 * (1.0 + sin(self.tick / 15 + (s / 16 * pi))) * 75)
                if distance(i) <= target:
                    pixels[s][i] = Color(hue=hue, saturation=1.0, luminance=0.5)
                else:
                    pixels[s][i] = Color('black')
            #     hue = (base_hue + 0.33 * (0.5 - math.sin(i_pct*math.pi))) % 1.0
            #     sat = math.fabs(math.sin((i_pct + s_pct) * math.pi))
            #     pixels[i] = Color(hue=hue, luminance=lum_pct, saturation=sat)

        self.tick += 1
