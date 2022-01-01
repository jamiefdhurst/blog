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

def test_index(client):
    response = client.get('/')
    assert b'Blog' in response.data
