'''Adds sizing and loading hints to rendered <img> tags.

Markdown gives us bare <img src alt> tags. Without intrinsic dimensions the
browser cannot reserve space, so every image shifts the text as it arrives,
and without a loading hint every image on a page is fetched up front.
'''
import os
import re
from PIL import Image

FIND_IMG = re.compile(r'<img\s([^>]*?)\s*/?>')
FIND_SRC = re.compile(r'src="([^"]+)"')

STATIC_ROOT = 'blog'

_dimensions = {}


def get_dimensions(src, static_root=STATIC_ROOT):
    '''Width and height of a rendered src path, or None if it cannot be read'''
    if src in _dimensions:
        return _dimensions[src]

    path = os.path.join(static_root, src.lstrip('/'))
    try:
        with Image.open(path) as image:
            size = image.size
    except (FileNotFoundError, OSError):
        size = None

    _dimensions[src] = size
    return size


def add_image_attributes(html, lazy=True, static_root=STATIC_ROOT):
    '''Add width, height, loading and decoding to every img tag in html'''
    if not html:
        return html

    def replace(match):
        attributes = match.group(1)
        src = FIND_SRC.search(attributes)
        if not src:
            return match.group(0)

        extra = []
        size = get_dimensions(src.group(1), static_root)
        if size and 'width=' not in attributes:
            extra.append(f'width="{size[0]}" height="{size[1]}"')

        if 'loading=' not in attributes:
            # The hero is above the fold, so deferring it would delay the
            # largest paint rather than help it.
            extra.append('loading="lazy"' if lazy
                         else 'loading="eager" fetchpriority="high"')
        if 'decoding=' not in attributes:
            extra.append('decoding="async"')

        if not extra:
            return match.group(0)
        return f'<img {attributes} {" ".join(extra)} />'

    return FIND_IMG.sub(replace, html)
