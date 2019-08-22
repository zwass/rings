#!/usr/bin/env python

'''Helper functions to make color manipulations easier.'''

from __future__ import division
import math
import random

import colour


n_strips = 16
n_pixels = 150


def clear_pixels(pixels):
    for s in pixels:
        for i in range(len(s)):
            s[i] = Color('black')


def remap(x, oldmin, oldmax, newmin, newmax):
    '''Remap the float x from the range oldmin-oldmax to the range newmin-newmax

    Does not clamp values that exceed min or max.
    For example, to make a sine wave that goes between 0 and 256:
        remap(math.sin(time.time()), -1, 1, 0, 256)

    '''
    zero_to_one = (x-oldmin) / (oldmax-oldmin)
    return zero_to_one*(newmax-newmin) + newmin

def clamp(x, minn, maxx):
    '''Restrict the float x to the range minn-maxx.'''
    return max(minn, min(maxx, x))

def cos(x, offset=0, period=1, minn=0, maxx=1):
    '''A cosine curve scaled to fit in a 0-1 range and 0-1 domain by default.

    offset: how much to slide the curve across the domain (should be 0-1)
    period: the length of one wave
    minn, maxx: the output range

    '''
    value = math.cos((x/period - offset) * math.pi * 2) / 2 + 0.5
    return value*(maxx-minn) + minn

def contrast(color, center, mult):
    '''Expand the color values by a factor of mult around the pivot value of center.

    color: an (r, g, b) tuple
    center: a float -- the fixed point
    mult: a float -- expand or contract the values around the center point

    '''
    r, g, b = color
    r = (r - center) * mult + center
    g = (g - center) * mult + center
    b = (b - center) * mult + center
    return (r, g, b)

def clip_black_by_luminance(color, threshold):
    '''If the color's luminance is less than threshold, replace it with black.

    color: an (r, g, b) tuple
    threshold: a float

    '''
    r, g, b = color
    if r+g+b < threshold*3:
        return (0, 0, 0)
    return (r, g, b)

def clip_black_by_channels(color, threshold):
    '''Replace any individual r, g, or b value less than threshold with 0.

    color: an (r, g, b) tuple
    threshold: a float

    '''
    r, g, b = color
    if r < threshold: r = 0
    if g < threshold: g = 0
    if b < threshold: b = 0
    return (r, g, b)

def mod_dist(a, b, n):
    '''Return the distance between floats a and b, modulo n.

    The result is always non-negative.
    For example, thinking of a clock:
    mod_dist(11, 1, 12) == 2 because you can 'wrap around'.

    '''
    return min((a-b) % n, (b-a) % n)

def gamma(color, gamma):
    '''Apply a gamma curve to the color.  The color values should be in the range 0-1.'''
    r, g, b = color
    return (max(r, 0) ** gamma, max(g, 0) ** gamma, max(b, 0) ** gamma)


class Color(colour.Color):
    def get_rgb_255(self):
        return tuple(int(255 * x) for x in self.rgb)

    def set_rgb_255(self, value):
        self.set_rgb(tuple(v / 255.0 for v in value))

    def scale_luminance(self, scale):
        scale = max(-1.0, min(1.0, scale))
        lum = self.get_luminance()
        lum = lum + scale * (1.0 - lum if scale > 0 else lum)
        self.set_luminance(lum)

    def scale_saturation(self, scale):
        scale = max(-1.0, min(1.0, scale))
        sat = self.get_saturation()
        sat = sat + scale * (1.0 - sat if scale > 0 else sat)
        self.set_saturation(sat)

    def interpolate_rgb(self, target, steps, step):
        t = float(step) / steps
        return Color(rgb=(
            self.red + t * (target.red - self.red),
            self.green + t * (target.green - self.green),
            self.blue + t * (target.blue - self.blue),
        ))

    def rgb_gradient(self, target, steps):
        return [self.interpolate_rgb(target, steps, s) for s in range(steps)]

    def clip_black(self, threshold):
        if self.get_luminance() < threshold:
            self.set_luminance(0)

def multiple_gradient(colors, steps):
    substeps = int(float(steps) / (len(colors) - 1))
    return list((
        c for l in (
            start.rgb_gradient(target, substeps)
            for start, target in zip(colors, colors[1:])
        ) for c in l
    ))


def make_gradient(n_colors, *colors):
    return multiple_gradient(
        [Color('#'+c) for c in colors],
        n_colors,
    )


schemes = {
    'dopely17': ['86E3CE', 'D0E6A5', 'FFDD94', 'FA897B', 'CCABD8'],
    'dopely18': ['D9ECF2', 'F56A79', 'FF414D', '1AA6B7', '002D40'],
    'dopely20': ['E25B45', 'FF8357', 'FAC172', '89D5C9', 'ADC865'],
    'dopely22': ['E2474B', '2F3A56', '406D96', 'A8D0DA', 'D8E8E8'],
    'dopely24': ['FCF5EF', 'FEA735', 'FE7235', '00C3FF', '0077FF'],
    'dopely95': ['041B2D', '004E9A', '428CD4', 'FF9CDA', 'EA4492'],
    'dopely97': ['35BBCA', '0191B4', 'F8D90F', 'D3DD18', 'FE7A15'],
    'dopely102': ['6AAB9C', 'FA9284', 'E06C78', '5874DC', '384E78'],
    'dopely103': ['7C5EFD', '99EEEE', 'F7BC23', 'FF4848', '000000'],
    'dopely105': ['031B88', '6096FD', 'AAB6FB', 'FB7B8E', 'FAA7B8'],
    'dopely109': ['205072', '329D9C', '56C596', '7BE495', 'CFF4D2'],
    'dopely113': ['7BD5F5', '787FF6', '787FF6', '1CA7EC', '1F2F98'],
    'dopely117': ['1039A0', '0146F2', 'FFD664', 'FF1684', 'FFFFFF'],
    'dopely124': ['7A7E8C', 'BFCAF7', 'AF49AB', 'DCD346', 'DF3F46'],
    'dopely128': ['F90202', 'F97F02', 'FFED00', '5DFF00', '00DDFF'],
    'dopely136': ['2D4B65', '4378A2', 'AF4474', 'F4C434', '9ACC8F'],
    'dopely137': ['01689C', '007F9F', '1EB0BB', '009B6A', '0FA982'],
    'dopely138': ['326199', '4FB1A1', 'FCC055', 'EB8D50', 'DF6E5B'],
    'dopely139': ['43045F', '4E0362', 'C63264', 'FF9799', 'FFBAAB'],
    'dopely143': ['125488', '2A93D5', '37CAEC', '3DD9D6', 'ADD9D8'],
    'dopely144': ['231F20', '426C95', 'F15F4E', 'F4D550', 'FAF7D8'],
    'dopely146': ['F392A3', '85D0CC', 'FDD194', '94D0FD', 'C9CBA5'],
    'dopely155': ['F2C6F2', 'B561BF', 'A6D1FF', '3988E1', '5B9252'],
    'dopely156': ['C8BD00', 'A44F6E', '3F1A34', '005B95', '002644'],
    'dopely157': ['F8EC6C', 'EF895D', 'B73A5D', '6A2B6F', '3AA6B7'],
    'dopely158': ['2960DE', 'F5E53A', '96B2FB', 'FFD3D4', 'DB5629'],
    'dopely164': ['8ECAE6', '209EBB', '023047', 'FFB701', 'FC8500'],
    'dopely165': ['A637A0', '933FA1', 'FFCF04', 'DF665D', '9FAEC3'],
    'dopely177': ['FC122C', 'C80058', '821963', '3D2250', '121525'],
    'dopely183': ['373442', '1D5562', 'FFE6D5', 'FFC48F', 'ED4B56'],
    'dopely191': ['ED3A78', 'FC5D47', 'ED8D09', 'C4B800', '80DD40'],
    'pineapple': ['054ba6', '0568a6', '0a8cbf', '6cbad9', 'f2b035'],
}


def create_palette(n_pixels, scheme=None):
    if scheme is None:
        scheme = random.choice(list(schemes.values()))
    scheme.append(scheme[0])
    return make_gradient(n_pixels, *scheme)


def pick_color(palette, i):
    return Color(palette[int(i) % len(palette)])


def rotate_array(arr, n):
    n = n % len(arr)
    tmp = arr[0:n]
    arr = arr[n:]
    arr += tmp
    return arr
