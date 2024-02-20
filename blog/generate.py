import os
import shutil
import sys
from jinja2 import Environment, PackageLoader, select_autoescape
from .articles import *
from .config import *

env = Environment(
    loader=PackageLoader('blog'),
    autoescape=select_autoescape()
)

def render_template(file, **kwargs):
    template = env.get_template(file)
    return template.render(**kwargs, version=VERSION)

def generate(articles_dir=ARTICLES_DIR, dist_dir=DIST_DIR):
    
    # Create/clear dist folder
    if os.path.isdir(dist_dir):
        print('[INFO] Clearing existing output dir...')
        shutil.rmtree(dist_dir)
    print('[INFO] Creating output dir...')
    os.mkdir(dist_dir)

    # Get all articles and generate a page for each one
    print('[INFO] Loading articles...')
    items = get_all_articles(articles_dir)
    print('[INFO] Loaded {} articles...'.format(len(items)))
    for item in items:
        print('[INFO] Rendering and writing {}...'.format(item.get_name()))
        rendered = render_template('view.html', article=item)
        with open(dist_dir + item.get_name() + '.html', 'w') as output_file:
            output_file.write(rendered)

    # Generate sitemap
    print('[INFO] Rendering and writing sitemap...')
    rendered = render_template('sitemap.xml', articles=items)
    with open(dist_dir + 'sitemap.xml', 'w') as output_file:
        output_file.write(rendered)

    # Generate static pages (inc error pages)
    for static_page in  ['404', '500', 'now']:
        print('[INFO] Rendering and writing {}...'.format(static_page))
        rendered = render_template(static_page + '.html')
        with open(dist_dir + static_page + '.html', 'w') as output_file:
            output_file.write(rendered)

    # Generate home page and paginated elements
    pages = get_pages(articles_dir)
    print('[INFO] Found {} pages of articles...'.format(pages))
    for p in range(1, pages + 1):
        print('[INFO] Rendering and writing index page {}...'.format(p))
        paged_items = get_paginated_articles(articles_dir, p)
        rendered = render_template(
            'index.html',
            articles=paged_items,
            current_page=p,
            pages=[None] * pages
        )
        with open(dist_dir + 'index.html' if p == 1 else dist_dir + 'index-{}.html'.format(p), 'w') as output_file:
            output_file.write(rendered)

    # Copy static assets
    print('[INFO] Copying static assets...')
    shutil.copytree('blog/static', dist_dir + 'static')
    
    print('Blog {} generated and output to {}'.format(VERSION, dist_dir))

if __name__ == '__main__':
    sys.exit(generate())
