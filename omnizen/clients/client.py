"""
This module provides the main client functionality for interacting with the Zendesk service.
"""

import logging
from typing import Optional
import requests
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from omnizen.settings import settings


logger = logging.getLogger("omnizen.client")


class ZendeskAPIClient:
    """
    A client to interact with the Zendesk API, supporting basic CRUD operations.
    """

    def __init__(
        self,
        domain: str = settings.domain,
        email: str = settings.email,
        api_token: str = settings.api_token,
    ):
        """
        Initializes the ZendeskAPIClient with the provided credentials.
        """
        self.domain = domain
        self.email = email
        self.api_token = api_token

        self._base_url = f"https://{domain}.zendesk.com/api/v2"
        self._session = requests.Session()
        _retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[404, 429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
            raise_on_status=False,
        )
        self._session.auth = HTTPBasicAuth(f"{self.email}/token", self.api_token)
        self._session.headers.update({"Content-Type": "application/json"})
        self._session.params = {"locale": "en"}

        _adapter = HTTPAdapter(max_retries=_retries)
        self._session.mount("https://", _adapter)
        self._session.mount("http://", _adapter)

    def get(
        self, endpoint: str, params: Optional[dict] = None, timeout: int = 10
    ) -> requests.Response:
        """
        Sends a GET request to the Zendesk API.
        """
        return self._session.get(
            f"{self._base_url}{endpoint}",
            params=params,
            timeout=timeout,
        )

    def post(
        self,
        endpoint: str,
        data: dict,
        params: Optional[dict] = None,
        timeout: int = 10,
    ) -> requests.Response:
        """
        Sends a POST request to the Zendesk API.
        """
        logger.debug(f"Sending POST {endpoint} | Data {data}")
        return self._session.post(
            f"{self._base_url}{endpoint}",
            json=data,
            timeout=timeout,
            params=params,
        )

    def patch(
        self,
        endpoint: str,
        data: dict,
        params: Optional[dict] = None,
        timeout: int = 10,
    ) -> requests.Response:
        """
        Sends a PATCH request to the Zendesk API.
        """
        logger.debug(f"Sending PATCH {endpoint} | Data {data}")
        return self._session.patch(
            f"{self._base_url}{endpoint}",
            json=data,
            timeout=timeout,
            params=params,
        )

    def put(
        self,
        endpoint: str,
        data: dict,
        params: Optional[dict] = None,
        timeout: int = 10,
    ) -> requests.Response:
        """
        Sends a PUT request to the Zendesk API.
        """
        logger.debug(f"Sending PUT {endpoint} | Data {data}")
        return self._session.put(
            f"{self._base_url}{endpoint}",
            json=data,
            timeout=timeout,
            params=params,
        )

    def delete(
        self, endpoint: str, params: Optional[dict] = None, timeout: int = 10
    ) -> requests.Response:
        """
        Sends a DELETE request to the Zendesk API.
        """
        logger.debug(f"Sending DELETE {endpoint}")
        return self._session.delete(
            f"{self._base_url}{endpoint}",
            timeout=timeout,
            params=params,
        )

    def upload_file(
        self, filename: str, content: bytes, timeout: int = 10
    ) -> requests.Response:
        """
        Uploads a file to Zendesk.
        """
        return self._session.post(
            f"{self._base_url}/uploads",
            headers={"Content-Type": "application/binary"},
            data=content,
            params={"filename": filename},
            timeout=timeout,
        )

    def __enter__(self):
        """
        Context manager entry method.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit method.
        """
        self._session.close()
