"""
This module provides the main client functionality for interacting with the Zendesk service.
"""

import json
import logging
from os import getenv
import requests
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


logger = logging.getLogger("omnizen.client")


class ZendeskAPIClient:
    """
    A client to interact with the Zendesk API, supporting basic CRUD operations.
    """

    def __init__(
        self,
        domain=getenv("ZENDESK_SUBDOMAIN", "mockdomain"),
        email=getenv("ZENDESK_EMAIL", "mock@mock.com"),
        api_token=getenv("ZENDESK_API_TOKEN", "mock_token"),
    ):
        """
        Initializes the ZendeskAPIClient with the provided credentials.
        """
        self.base_url = f"https://{domain}.zendesk.com/api/v2"
        self.email = email
        self.api_token = api_token
        self.auth = HTTPBasicAuth(f"{self.email}/token", self.api_token)
        self.default_params = {"locale": "en"}
        self.headers = {"Content-Type": "application/json"}

        self.session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[404, 429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
            raise_on_status=False,
        )

        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _handle_response(self, response):
        """
        Handles the response from the Zendesk API, checking for errors and returning JSON data.
        """
        try:
            return {
                "data": response.json(),
                "status_code": response.status_code,
            }
        except json.JSONDecodeError as json_error:
            return {
                "error": {"title": response.text, "message": str(json_error)},
                "status_code": response.status_code,
            }

    def get(self, endpoint, params=None, timeout=10):
        """
        Sends a GET request to the Zendesk API.
        """
        params = {**self.default_params, **(params or {})}
        response = self.session.get(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            params=params,
            auth=self.auth,
            timeout=timeout,
        )
        return self._handle_response(response)

    def post(self, endpoint, data, params=None, timeout=10):
        """
        Sends a POST request to the Zendesk API.
        """
        logger.info(f"Sending POST {endpoint} | Data {data}")
        params = {**self.default_params, **(params or {})}
        response = self.session.post(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            json=data,
            auth=self.auth,
            timeout=timeout,
            params=params,
        )
        return self._handle_response(response)

    def patch(self, endpoint, data, params=None, timeout=10):
        """
        Sends a PATCH request to the Zendesk API.
        """
        logger.info(f"Sending PATCH {endpoint} | Data {data}")
        params = {**self.default_params, **(params or {})}
        response = self.session.patch(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            json=data,
            auth=self.auth,
            timeout=timeout,
            params=params,
        )
        return self._handle_response(response)

    def put(self, endpoint, data, params=None, timeout=10):
        """
        Sends a PUT request to the Zendesk API.
        """
        logger.info(f"Sending PUT {endpoint} | Data {data}")
        params = {**self.default_params, **(params or {})}
        response = self.session.put(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            json=data,
            auth=self.auth,
            timeout=timeout,
            params=params,
        )
        return self._handle_response(response)

    def delete(self, endpoint, params=None, timeout=10):
        """
        Sends a DELETE request to the Zendesk API.
        """
        logger.info(f"Sending DELETE {endpoint}")
        params = {**self.default_params, **(params or {})}
        response = self.session.delete(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            auth=self.auth,
            timeout=timeout,
            params=params,
        )
        return self._handle_response(response)

    def upload_file(self, filename: str, content: bytes, timeout: int = 10) -> dict:
        """
        Uploads a file to Zendesk.
        """
        response = self.session.post(
            f"{self.base_url}/uploads",
            headers={"Content-Type": "application/binary"},
            data=content,
            auth=self.auth,
            params={"filename": filename},
            timeout=timeout,
        )
        return self._handle_response(response)
