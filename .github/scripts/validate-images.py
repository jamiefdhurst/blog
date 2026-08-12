#!/usr/bin/env python3
'''Fail the build if an image in blog/static is too large or too wide.

Images are the dominant cost of a page here, so this guards the two things
that actually matter: an unresized camera original (caught by width) and a
badly compressed file (caught by size).

Run `python .github/scripts/optimise-images.py` to fix anything reported.
'''
import os
import sys
from PIL import Image

STATIC_DIR = 'blog/static'
MAX_WIDTH = 1400          # matches optimise-images.py
MAX_BYTES = 800 * 1024
# Icons are referenced at fixed sizes by the manifest and link tags, so they
# are exempt from the width rule - they are tiny regardless.
ICONS = ('favicon', 'apple-touch-icon', 'android-chrome', 'mstile', 'safari-pinned')


def is_icon(name):
    return any(name.startswith(prefix) for prefix in ICONS)


def main():
    failures = []
    checked = 0
    total = 0

    for name in sorted(os.listdir(STATIC_DIR)):
        if not name.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
        path = os.path.join(STATIC_DIR, name)
        size = os.path.getsize(path)
        checked += 1
        total += size

        with Image.open(path) as image:
            width, _ = image.size
            image_format = image.format

        if size > MAX_BYTES:
            failures.append(f'{name}: {size / 1024:.0f}K exceeds the '
                            f'{MAX_BYTES / 1024:.0f}K limit')
        if width > MAX_WIDTH and not is_icon(name):
            failures.append(f'{name}: {width}px wide exceeds the {MAX_WIDTH}px limit')

        # A .jpg holding PNG data (or vice versa) is served with the wrong
        # content type and is usually many times larger than it should be.
        expected = 'JPEG' if name.lower().endswith(('.jpg', '.jpeg')) else 'PNG'
        if image_format not in (expected, 'MPO'):
            failures.append(f'{name}: contains {image_format} data '
                            f'but has a {expected} extension')

    print(f'Checked {checked} images, {total / 1048576:.1f} MB total')

    if failures:
        print(f'\n{len(failures)} image problem(s):\n')
        for failure in failures:
            print(f'  ✗ {failure}')
        print('\nRun: python .github/scripts/optimise-images.py')
        return 1

    print('All images within limits')
    return 0


if __name__ == '__main__':
    sys.exit(main())
