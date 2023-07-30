import pytest

from blog import create_app


@pytest.fixture
def app():
    app = create_app({
        'ARTICLES_DIR': 'tests/articles/',
        'TESTING': True,
        'VERSION': 'DEVELOPMENT',
    })

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
