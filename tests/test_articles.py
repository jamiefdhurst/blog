from blog.articles import *

def test_get_article():
    get_article('tests/articles/', '2022-01-01_test-1')

def test_article_failure():
    err = None
    try:
        get_article('tests/articles/', '2022-01-01_not-found')
    except ArticleNotFoundException as e:
        err = e
    assert err is not None

def test_get_paginated_articles():
    sut = get_paginated_articles('tests/articles/')
    assert len(sut) == 2
    assert sut[0].get_name() == '2022-01-02_test-2'

def test_get_paginated_articles_multiple_pages():
    sut = get_paginated_articles('tests/articles/', 1, 1)
    assert len(sut) == 1
    assert sut[0].get_name() == '2022-01-02_test-2'

def test_get_paginated_articles_out_of_range():
    sut = get_paginated_articles('tests/articles/', 2, 10)
    assert len(sut) == 0

def test_get_all_articles():
    sut = get_all_articles('tests/articles/')
    assert len(sut) == 2
    assert sut[0].get_name() == '2022-01-02_test-2'

def test_get_pages():
    assert get_pages('tests/articles/') == 1

def test_article_get_contents():
    sut = Article('tests/articles/', '2022-01-01_test-1.md')
    assert '<h1>Test 1</h1>' in sut.get_contents()
    assert '<img alt="Placeholder" src="/static/placeholder.png" />' in sut.get_contents()
    assert '<h2>A test article that has very little inside of it.</h2>' in sut.get_contents()
    assert '<p>They were just sucked into space.' in sut.get_contents()

def test_article_get_content_only():
    sut = Article('tests/articles/', '2022-01-01_test-1.md')
    assert '<h1>Test 1</h1>' not in sut.get_content_only()
    assert '<img alt="Placeholder" src="/static/placeholder.png" />' in sut.get_content_only()
    assert '<h2>A test article that has very little inside of it.</h2>' not in sut.get_content_only()
    assert '<p>They were just sucked into space.' in sut.get_content_only()

def test_article_get_content_only_no_summary():
    sut = Article('tests/articles/', '2022-01-02_test-2.md')
    assert '<h1>Test 1</h1>' not in sut.get_content_only()
    assert '<img alt="Placeholder" src="/static/placeholder.png" />' in sut.get_content_only()
    assert '<p>Worf, It\'s better than music.' in sut.get_content_only()

def test_article_get_date():
    sut = Article('tests/articles/', '2022-01-01_test-1.md')
    assert datetime.datetime(2022, 1, 1, 0, 0) == sut.get_date()

def test_article_get_date_failure():
    err = None
    try:
        sut = Article('tests/failed-articles/', 'no-date.md')
        sut.get_date()
    except InvalidDateForArticleException as e:
        err = e
    assert err is not None

def test_article_get_image():
    sut = Article('tests/articles/', '2022-01-01_test-1.md')
    assert '<img alt="Placeholder" src="/static/placeholder.png" />' == sut.get_image()

def test_article_get_image_failure():
    sut = Article('tests/failed-articles/', '2022-01-01_no-image.md')
    assert sut.get_image() is None

def test_article_get_summary():
    sut = Article('tests/articles/', '2022-01-01_test-1.md')
    assert 'A test article that has very little inside of it.' == sut.get_summary()

def test_article_get_summary_missing():
    sut = Article('tests/articles/', '2022-01-02_test-2.md')
    assert sut.get_summary() is None

def test_article_get_title():
    sut = Article('tests/articles/', '2022-01-01_test-1.md')
    assert 'Test 1' == sut.get_title()

def test_article_get_title_failure():
    err = None
    try:
        sut = Article('tests/failed-articles/', '2022-01-03_no-title.md')
        sut.get_title()
    except InvalidTitleForArticleException as e:
        err = e
    assert err is not None
