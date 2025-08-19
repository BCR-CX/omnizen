"""
Tests for the Omnizen async client module.
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import httpx

from omnizen.clients.async_client import AsyncZendeskAPIClient


@pytest.mark.asyncio
async def test_async_client_init():
    """Test AsyncZendeskAPIClient initialization."""
    email = "test@test.com"
    api_token = "test_token"
    domain = "test_domain"

    client = AsyncZendeskAPIClient(email=email, api_token=api_token, domain=domain)

    assert client.domain == domain
    assert client.email == email
    assert client.api_token == api_token
    assert client._base_url == f"https://{domain}.zendesk.com/api/v2"
    assert isinstance(client._client.auth, httpx.BasicAuth)
    assert client._client.headers["Content-Type"] == "application/json"
    assert client._client.params["locale"] == "en"
    assert isinstance(client._transport, httpx.AsyncHTTPTransport)

    await client.aclose()


@pytest.mark.asyncio
async def test_http_methods():
    """Test all HTTP methods with and without parameters."""
    async with AsyncZendeskAPIClient() as client:
        with patch.object(client._client, "get") as mock_get:
            mock_get.return_value = MagicMock(status_code=200)
            response = await client.get("/test")
            assert response.status_code == 200
            mock_get.assert_called_once_with("/test", params=None)

        with patch.object(client._client, "post") as mock_post:
            mock_post.return_value = MagicMock(status_code=201)
            response = await client.post("/test", data={"name": "test"})
            assert response.status_code == 201
            mock_post.assert_called_once_with(
                "/test", json={"name": "test"}, params=None
            )

        with patch.object(client._client, "patch") as mock_patch:
            mock_patch.return_value = MagicMock(status_code=200)
            response = await client.patch("/test/1", data={"name": "updated"})
            assert response.status_code == 200
            mock_patch.assert_called_once_with(
                "/test/1", json={"name": "updated"}, params=None
            )

        with patch.object(client._client, "put") as mock_put:
            mock_put.return_value = MagicMock(status_code=200)
            response = await client.put("/test/1", data={"name": "replaced"})
            assert response.status_code == 200
            mock_put.assert_called_once_with(
                "/test/1", json={"name": "replaced"}, params=None
            )

        with patch.object(client._client, "delete") as mock_delete:
            mock_delete.return_value = MagicMock(status_code=204)
            response = await client.delete("/test/1")
            assert response.status_code == 204
            mock_delete.assert_called_once_with("/test/1", params=None)


@pytest.mark.asyncio
async def test_upload_file():
    """Test file upload functionality."""
    async with AsyncZendeskAPIClient() as client:
        with patch.object(client._client, "post") as mock_post:
            mock_post.return_value = MagicMock(status_code=201)

            content = b"test file content"
            filename = "test.txt"
            response = await client.upload_file(filename=filename, content=content)

            assert response.status_code == 201
            mock_post.assert_called_once_with(
                "/uploads",
                headers={"Content-Type": "application/binary"},
                content=content,
                params={"filename": filename},
            )


@pytest.mark.asyncio
async def test_error_handling():
    """Test error response handling."""
    async with AsyncZendeskAPIClient() as client:
        with patch.object(client._client, "get") as mock_get:
            mock_get.return_value = MagicMock(status_code=500)
            response = await client.get("/test")
            assert response.status_code == 500

            mock_get.side_effect = httpx.ConnectError("Connection failed")
            with pytest.raises(httpx.ConnectError):
                await client.get("/test")

            mock_get.side_effect = httpx.TimeoutException("Request timeout")
            with pytest.raises(httpx.TimeoutException):
                await client.get("/test")


@pytest.mark.asyncio
async def test_context_manager():
    """Test async context manager functionality."""
    async with AsyncZendeskAPIClient() as client:
        assert isinstance(client, AsyncZendeskAPIClient)
        assert hasattr(client, "_client")

    client = AsyncZendeskAPIClient()
    with patch.object(client._client, "aclose") as mock_close:
        mock_close.return_value = AsyncMock()
        await client.aclose()
        mock_close.assert_called_once()
