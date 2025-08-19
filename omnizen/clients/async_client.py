import logging
from typing import Optional
import httpx

from omnizen.settings import settings

logger = logging.getLogger("omnizen.async_client")


class AsyncZendeskAPIClient:
    """
    Async client to interact with the Zendesk API with retry and session management.
    """

    def __init__(
        self,
        domain: str = settings.domain,
        email: str = settings.email,
        api_token: str = settings.api_token,
    ):
        """
        Initializes the AsyncZendeskAPIClient with the provided credentials and retry configuration.
        """

        self.domain = domain
        self.email = email
        self.api_token = api_token
        self._base_url = f"https://{domain}.zendesk.com/api/v2"

        self._transport = httpx.AsyncHTTPTransport(
            retries=3,
        )

        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            auth=(f"{self.email}/token", self.api_token),
            headers={"Content-Type": "application/json"},
            params={"locale": "en"},
            follow_redirects=True,
            transport=self._transport,
        )

    async def get(self, endpoint: str, params: Optional[dict] = None) -> httpx.Response:
        """
        Sends a async GET request to the Zendesk API.
        """
        logger.debug(f"Sending GET {endpoint} | Params {params}")
        return await self._client.get(
            endpoint,
            params=params,
        )

    async def post(
        self, endpoint: str, data: dict, params: Optional[dict] = None
    ) -> httpx.Response:
        """
        Sends a async POST request to the Zendesk API.
        """
        logger.debug(f"Sending POST {endpoint} | Data {data}")
        return await self._client.post(endpoint, json=data, params=params)

    async def patch(
        self, endpoint: str, data: dict, params: Optional[dict] = None
    ) -> httpx.Response:
        """
        Sends a async PATCH request to the Zendesk API.
        """
        logger.debug(f"Sending PATCH {endpoint} | Data {data}")
        return await self._client.patch(endpoint, json=data, params=params)

    async def put(
        self, endpoint: str, data: dict, params: Optional[dict] = None
    ) -> httpx.Response:
        """
        Sends a async PUT request to the Zendesk API.
        """
        logger.debug(f"Sending PUT {endpoint} | Data {data}")
        return await self._client.put(endpoint, json=data, params=params)

    async def delete(
        self, endpoint: str, params: Optional[dict] = None
    ) -> httpx.Response:
        """
        Sends a async DELETE request to the Zendesk API.
        """
        logger.debug(f"Sending DELETE {endpoint}")
        return await self._client.delete(endpoint, params=params)

    async def upload_file(self, filename: str, content: bytes) -> httpx.Response:
        return await self._client.post(
            "/uploads",
            headers={"Content-Type": "application/binary"},
            content=content,
            params={"filename": filename},
        )

    async def aclose(self):
        """
        Closes the async client session.
        """
        await self._client.aclose()

    async def __aenter__(self):
        """
        Context manager entry method to allow usage with 'async with'.
        """

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit method to allow usage with 'async with'.
        """

        await self.aclose()
