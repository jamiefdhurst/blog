from blog import create_app

def test_config():
    assert not create_app().testing
    app = create_app({
        'ARTICLES_DIR': 'tests/articles/',
        'GITHUB_USERNAME': 'jamiefdhurst',
        'GITHUB_TOKEN': 'example',
        'TESTING': True})
    assert app.testing
    assert app.config['ARTICLES_DIR'] == 'tests/articles/'
    assert app.config['GITHUB_USERNAME'] == 'jamiefdhurst'
    assert app.config['GITHUB_TOKEN'] == 'example'

def test_github_empty_response(mock_github_request_empty_response, client):
    response = client.get('/')
    assert b'System DEVELOPMENT' in response.data

def test_github_successful_response(mock_github_request, client):
    response = client.get('/')
    assert b'System v1.0-TEST' in response.data

def test_404(client):
    response = client.get('/not-found-path')
    assert b'Page Not Found' in response.data
    assert 404 == response.status_code
