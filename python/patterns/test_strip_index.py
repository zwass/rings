from .base_pattern import BasePattern
from .utils import Color, clear_pixels


class TestStripIndex(BasePattern):
    name = 'Test Strip Index'

    def __init__(self):
        self.tick = 0

    def render(self, pixels):
        clear_pixels(pixels)

        for i, s in enumerate(pixels):
            for p in range(i+1):
                if p % 5 == 0:
                    s[p] = Color('blue')
                else:
                    s[p] = Color('red')

        self.tick += 1
