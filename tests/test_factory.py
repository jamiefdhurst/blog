from blog import create_app

def test_config():
    assert not create_app().testing
    app = create_app({
        'ARTICLES_DIR': 'tests/articles/',
        'TESTING': True})
    assert app.testing
    assert app.config['ARTICLES_DIR'] == 'tests/articles/'

def test_404(client):
    response = client.get('/not-found-path')
    assert b'Page Not Found' in response.data
    assert 404 == response.status_code
