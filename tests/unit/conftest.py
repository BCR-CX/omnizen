import pytest
from omnizen.settings import settings

BASE_URL = f"https://{settings.domain}.zendesk.com/api/v2"


@pytest.fixture
def client():
    from omnizen.client import ZendeskAPIClient

    return ZendeskAPIClient()


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


@pytest.fixture
def concret_base_model():
    from omnizen.models.base import BulkResponse
    from omnizen.models.base import BaseModel

    class TestConcreteModel(BaseModel):
        def save(self):
            return None

        def delete(self):
            return None

        def refresh(self):
            return None

        @classmethod
        def get(cls, id):
            return cls()

        @classmethod
        def all(cls):
            return [cls()]

        @classmethod
        def filter(cls, query):
            return [cls()]

        @classmethod
        def search(cls, word: str):
            return [cls()]

        @classmethod
        def count(cls):
            return 1

        @classmethod
        def bulk_create(cls, items, fields=None, wait_to_complete=False, sleep=0.1):
            return None

        @classmethod
        def bulk_update(cls, items, fields=None, wait_to_complete=False, sleep=0.1):
            return None

        @classmethod
        def bulk_delete(cls, items, fields=None, wait_to_complete=False, sleep=0.1):
            return None

        @classmethod
        def _format_bulk_response(cls, response):
            data: BulkResponse = {"success": [], "errors": []}
            return data

        @classmethod
        def _format_record(cls: type, record: dict):
            return cls(**record)

    return TestConcreteModel


@pytest.fixture
def color_choices():
    from omnizen.fields.types import Choices

    class ColorChoices(Choices):
        RED = "red"
        GREEN = "green"
        BLUE = "blue"

    return ColorChoices


@pytest.fixture
def color_choice_with_labels():
    from omnizen.fields.types import Choices

    class ColorChoiceWithLabels(Choices):
        RED = "red", "Red Color"
        GREEN = "green", "Green Color"
        BLUE = "blue", "Blue Color"

    return ColorChoiceWithLabels
