import os
import shutil
import sys
from jinja2 import Environment, PackageLoader, select_autoescape
from .articles import get_all_articles, get_paginated_articles, get_pages
from .config import ARTICLES_DIR, DIST_DIR, VERSION

env = Environment(
    loader=PackageLoader('blog'),
    autoescape=select_autoescape()
)

def render_template(file, **kwargs):
    template = env.get_template(file)
    return template.render(**kwargs, version=VERSION)

def generate(articles_dir=ARTICLES_DIR, dist_dir=DIST_DIR):

    # Create/clear dist folder
    if not os.path.isdir(dist_dir):
        print('[INFO] Creating output dir...')
        os.mkdir(dist_dir)
    else:
        print('[INFO] Clearing existing output dir...')
        with os.scandir(dist_dir) as entries:
            for entry in entries:
                if entry.is_file():
                    os.unlink(entry.path)
                else:
                    shutil.rmtree(entry.path)

    # Get all articles and generate a page for each one
    print('[INFO] Loading articles...')
    items = get_all_articles(articles_dir)
    print(f'[INFO] Loaded {len(items)} articles...')
    for item in items:
        print(f'[INFO] Rendering and writing {item.get_name()}...')
        rendered = render_template('view.html', article=item)
        with open(dist_dir + item.get_name() + '.html', 'w', encoding='UTF-8') as output_file:
            output_file.write(rendered)

    # Generate sitemap
    print('[INFO] Rendering and writing sitemap...')
    rendered = render_template('sitemap.xml', articles=items)
    with open(dist_dir + 'sitemap.xml', 'w', encoding='UTF-8') as output_file:
        output_file.write(rendered)

    # Generate static pages (inc error pages)
    for static_page in  ['404', '500', 'now']:
        print(f'[INFO] Rendering and writing {static_page}...')
        rendered = render_template(static_page + '.html')
        with open(dist_dir + static_page + '.html', 'w', encoding='UTF-8') as output_file:
            output_file.write(rendered)

    # Generate home page and paginated elements
    pages = get_pages(articles_dir)
    print(f'[INFO] Found {pages} pages of articles...')
    for p in range(1, pages + 1):
        print(f'[INFO] Rendering and writing index page {p}...')
        paged_items = get_paginated_articles(articles_dir, p)
        rendered = render_template(
            'index.html',
            articles=paged_items,
            current_page=p,
            pages=[None] * pages
        )
        with open(dist_dir + 'index.html' if p == 1 else dist_dir +
                  f'index-{p}.html', 'w', encoding='UTF-8') as output_file:
            output_file.write(rendered)

    # Copy static assets
    print('[INFO] Copying static assets...')
    shutil.copytree('blog/static', dist_dir + 'static')

    print(f'Blog {VERSION} generated and written to {dist_dir}')

if __name__ == '__main__':
    sys.exit(generate())
