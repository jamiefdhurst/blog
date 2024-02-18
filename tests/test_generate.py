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
    assert os.path.exists('tests/dist/static')
    assert os.path.exists('tests/dist/static/css/default.min.css')
    assert os.path.exists('tests/dist/2022-01-01_test-1.html')
    assert os.path.exists('tests/dist/2022-01-02_test-2.html')
