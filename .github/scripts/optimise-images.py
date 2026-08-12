#!/usr/bin/env python3
'''Resize and optimise the images in blog/static in place.

Run this after adding new images:

    python .github/scripts/optimise-images.py

Images are never upscaled, and anything already within the limits is left
alone. The matching CI check is validate-images.py, which enforces the same
limits so an unoptimised image cannot reach main.
'''
import math
import os
import sys
from PIL import Image, ImageChops, ImageStat

STATIC_DIR = 'blog/static'
MAX_WIDTH = 1400        # content column is 700px, so this covers 2x displays
JPEG_QUALITY = 82
PNG_COLOURS = 256
# Quantising a PNG to a 256-colour palette is a big win on flat UI
# screenshots and invisible to the eye, but it bands photographic content
# such as gradients. Anything that degrades by more than this is kept
# lossless instead.
MAX_QUANTISE_RMSE = 3.0


def rmse(first, second):
    '''Root mean squared error between two images, on a 0-255 scale'''
    difference = ImageChops.difference(first.convert('RGB'), second.convert('RGB'))
    return math.sqrt(sum(band * band for band in ImageStat.Stat(difference).rms) / 3)


def resize(image):
    if image.width <= MAX_WIDTH:
        return image, False
    height = round(image.height * MAX_WIDTH / image.width)
    return image.resize((MAX_WIDTH, height), Image.LANCZOS), True


def save_jpeg(image, path):
    image.convert('RGB').save(
        path, 'JPEG', quality=JPEG_QUALITY, optimize=True, progressive=True)


def save_png(image, path):
    '''Save as a palette PNG when that does not visibly degrade the image'''
    if image.mode == 'RGBA' and image.getchannel('A').getextrema()[0] == 255:
        image = image.convert('RGB')

    lossless = path + '.lossless.tmp'
    image.save(lossless, 'PNG', optimize=True)

    quantised_image = image.quantize(colors=PNG_COLOURS, method=Image.FASTOCTREE)
    quantised = path + '.quantised.tmp'
    quantised_image.save(quantised, 'PNG', optimize=True)

    error = rmse(image, quantised_image)
    use_quantised = (error <= MAX_QUANTISE_RMSE
                     and os.path.getsize(quantised) < os.path.getsize(lossless))

    os.replace(quantised if use_quantised else lossless, path)
    os.unlink(lossless if use_quantised else quantised)
    return use_quantised, error


def optimise(path):
    '''Returns (bytes_before, bytes_after, note)'''
    before = os.path.getsize(path)
    extension = path.rsplit('.', 1)[1].lower()

    with Image.open(path) as opened:
        opened.load()
        image, resized = resize(opened)

        # Decide the output format from the extension, not the format Pillow
        # reports - phone cameras produce MPO files with a .jpg extension, and
        # writing those back out as PNG makes them many times larger.
        if extension in ('jpg', 'jpeg'):
            save_jpeg(image, path)
            note = 'jpeg'
        else:
            quantised, error = save_png(image, path)
            note = f'png {"quantised" if quantised else "lossless"} rmse={error:.2f}'

    if resized:
        note = f'resized->{MAX_WIDTH}px {note}'
    return before, os.path.getsize(path), note


def main():
    names = sorted(name for name in os.listdir(STATIC_DIR)
                   if name.lower().endswith(('.png', '.jpg', '.jpeg')))
    before_total = after_total = 0
    for name in names:
        before, after, note = optimise(os.path.join(STATIC_DIR, name))
        before_total += before
        after_total += after
        if before != after:
            print(f'  {name:52} {before/1024:8.0f}K -> {after/1024:7.0f}K  {note}')

    saved = before_total - after_total
    print(f'\n{len(names)} images: {before_total/1048576:.1f} MB -> '
          f'{after_total/1048576:.1f} MB (saved {saved/1048576:.1f} MB, '
          f'{100 * saved / before_total:.0f}%)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
