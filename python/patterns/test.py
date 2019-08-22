from .base_pattern import BasePattern
from .utils import Color, clear_pixels


class Test(BasePattern):
    name = 'Test Pattern'

    def __init__(self):
        self.tick = 0

    def render(self, pixels):
        clear_pixels(pixels)

        for i, s in enumerate(pixels):
            i += self.tick
            s[i % len(s)] = Color('red')
            s[(i+1) % len(s)] = Color('green')
            s[(i+2) % len(s)] = Color('blue')

        self.tick += 1
