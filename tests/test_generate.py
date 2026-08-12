from blog.generate import *
import os

def test_generate():
    generate(articles_dir='tests/articles/', dist_dir='tests/dist/')
    assert os.path.exists('tests/dist/')
    assert os.path.exists('tests/dist/404.html')
    assert os.path.exists('tests/dist/500.html')
    assert os.path.exists('tests/dist/index.html')
    assert os.path.exists('tests/dist/now.html')
    assert os.path.exists('tests/dist/sitemap.xml')
    assert os.path.exists('tests/dist/feed.xml')
    assert os.path.exists('tests/dist/robots.txt')
    assert os.path.exists('tests/dist/static')
    assert os.path.exists('tests/dist/static/css/default.min.css')
    assert os.path.exists('tests/dist/2022-01-01_test-1.html')
    assert os.path.exists('tests/dist/2022-01-02_test-2.html')

def test_generate_writes_feed_and_robots():
    generate(articles_dir='tests/articles/', dist_dir='tests/dist/')
    with open('tests/dist/feed.xml', encoding='UTF-8') as feed_file:
        feed = feed_file.read()
    assert '<rss version="2.0"' in feed
    assert '<item>' in feed
    with open('tests/dist/robots.txt', encoding='UTF-8') as robots_file:
        robots = robots_file.read()
    assert 'User-agent: *' in robots
    assert 'Sitemap: ' in robots

def test_generate_sitemap_has_lastmod_and_homepage():
    generate(articles_dir='tests/articles/', dist_dir='tests/dist/')
    with open('tests/dist/sitemap.xml', encoding='UTF-8') as sitemap_file:
        sitemap = sitemap_file.read()
    assert '<lastmod>' in sitemap
    assert '<loc>https://jamiehurst.co.uk/</loc>' in sitemap
