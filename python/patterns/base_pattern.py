from .utils import Color, n_strips, n_pixels, clear_pixels


class BasePattern:
    patterns = []
    patterns_map = {}

    # https://stackoverflow.com/questions/5189232/how-to-auto-register-a-class-when-its-defined
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.patterns.append(cls)
        cls.patterns_map[cls.name] = cls

    def __init__(self):
        self.pixels = [[Color('black')] * n_pixels for i in range(n_strips)]
        self.pattern = self.patterns_map['Center Waves']()

    def reset(self):
        clear_pixels(self.pixels)

    def render_pattern(self):
        self.pattern.render(self.pixels)

    def set_pattern(self, pattern):
        self.reset()
        self.pattern = self.patterns_map[pattern]()
