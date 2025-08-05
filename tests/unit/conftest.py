import pytest

DOMAIN = "test"
BASE_URL = "https://test.zendesk.com/api/v2"


@pytest.fixture
def client():
    from omnizen.client import ZendeskAPIClient

    return ZendeskAPIClient(domain=DOMAIN)


@pytest.fixture
def mock_response_200(requests_mock):
    requests_mock.get(f"{BASE_URL}/", json={}, status_code=200)


@pytest.fixture
def mock_response_500(requests_mock):
    requests_mock.get(f"{BASE_URL}/", json={}, status_code=500)


@pytest.fixture
def mock_response_not_serializable(requests_mock):
    requests_mock.get(f"{BASE_URL}/", status_code=500)


@pytest.fixture
def mock_upload_response_200(requests_mock):
    requests_mock.post(f"{BASE_URL}/uploads", json={}, status_code=201)
