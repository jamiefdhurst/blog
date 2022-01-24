import pytest

from blog import create_app


@pytest.fixture
def mock_github_request_empty_response(requests_mock):
    requests_mock.get(
        'https://api.github.com/repos/jamiefdhurst/blog/releases',
        json='',
    )


@pytest.fixture
def mock_github_request(requests_mock):
    requests_mock.get(
        'https://api.github.com/repos/jamiefdhurst/blog/releases',
        json=[{'name': 'v1.0-TEST'}],
    )


@pytest.fixture
def app():
    app = create_app({
        'ARTICLES_DIR': 'tests/articles/',
        'GITHUB_USERNAME': 'jamiefdhurst',
        'GITHUB_TOKEN': 'example',
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
