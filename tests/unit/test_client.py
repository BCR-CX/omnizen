"""
Tests for the Omnizen client module.
"""

import pytest
from unittest.mock import patch, MagicMock
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectTimeout, ReadTimeout
from http.client import HTTPMessage

from omnizen.client import ZendeskAPIClient


def test_client_init():
    """
    Test the initialization of the ZendeskAPIClient.
    """
    email = "test@test.com"
    api_token = "test_token"
    domain = "test_domain"

    client = ZendeskAPIClient(email=email, api_token=api_token, domain=domain)

    assert client.auth == HTTPBasicAuth(email + "/token", api_token)
    assert client.base_url == f"https://{domain}.zendesk.com/api/v2"


def test_auth_parameter_in_requests():
    """
    Test that the correct auth parameter is passed to all HTTP requests.
    """
    email = "test@example.com"
    api_token = "test_api_token"
    domain = "test_domain"

    client = ZendeskAPIClient(email=email, api_token=api_token, domain=domain)

    with patch.object(client.session, "get") as mock_get, patch.object(
        client.session, "post"
    ) as mock_post, patch.object(client.session, "patch") as mock_patch, patch.object(
        client.session, "put"
    ) as mock_put, patch.object(
        client.session, "delete"
    ) as mock_delete:

        mock_response = MagicMock()
        mock_response.json.return_value = {"test": "data"}
        mock_response.status_code = 200

        mock_get.return_value = mock_response
        mock_post.return_value = mock_response
        mock_patch.return_value = mock_response
        mock_put.return_value = mock_response
        mock_delete.return_value = mock_response

        # Test GET request
        client.get("/test")
        mock_get.assert_called_once()
        get_call_kwargs = mock_get.call_args.kwargs
        assert isinstance(get_call_kwargs["auth"], HTTPBasicAuth)
        assert get_call_kwargs["auth"].username == f"{email}/token"
        assert get_call_kwargs["auth"].password == api_token

        # Test POST request
        client.post("/test", {"data": "test"})
        mock_post.assert_called_once()
        post_call_kwargs = mock_post.call_args.kwargs
        assert isinstance(post_call_kwargs["auth"], HTTPBasicAuth)
        assert post_call_kwargs["auth"].username == f"{email}/token"
        assert post_call_kwargs["auth"].password == api_token

        # Test PATCH request
        client.patch("/test", {"data": "test"})
        mock_patch.assert_called_once()
        patch_call_kwargs = mock_patch.call_args.kwargs
        assert isinstance(patch_call_kwargs["auth"], HTTPBasicAuth)
        assert patch_call_kwargs["auth"].username == f"{email}/token"
        assert patch_call_kwargs["auth"].password == api_token

        # Test PUT request
        client.put("/test", {"data": "test"})
        mock_put.assert_called_once()
        put_call_kwargs = mock_put.call_args.kwargs
        assert isinstance(put_call_kwargs["auth"], HTTPBasicAuth)
        assert put_call_kwargs["auth"].username == f"{email}/token"
        assert put_call_kwargs["auth"].password == api_token

        # Test DELETE request
        client.delete("/test")
        mock_delete.assert_called_once()
        delete_call_kwargs = mock_delete.call_args.kwargs
        assert isinstance(delete_call_kwargs["auth"], HTTPBasicAuth)
        assert delete_call_kwargs["auth"].username == f"{email}/token"
        assert delete_call_kwargs["auth"].password == api_token


def test_client_response_ok(client, mock_response_200):
    """
    Test that the client handles successful responses correctly.
    """
    response = client.get("/")

    assert response["status_code"] == 200


def test_client_response_error(client, mock_response_500):
    """
    Test that the client handles error responses correctly.
    """
    response = client.get("/")

    assert response["status_code"] == 500


def test_upload_file_response_ok(client, mock_upload_response_200):
    """
    Test that the client handles successful file upload responses correctly.
    """
    response = client.upload_file(content=b"test", filename="test.txt")

    assert response["status_code"] == 201


def test_client_response_not_serializable(client, mock_response_not_serializable):
    """
    Test that the client handles non-serializable responses.
    """
    response = client.get("/")

    assert response["error"] == {
        "message": "Expecting value: line 1 column 1 (char 0)",
        "title": "",
    }


def test_default_timeout_parameter(client):
    """
    Test that default timeout is applied to requests.
    """
    with patch.object(client.session, "get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"test": "data"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        client.get("/test")

        mock_get.assert_called_once()
        call_kwargs = mock_get.call_args.kwargs
        assert call_kwargs["timeout"] == 10


def test_custom_timeout_parameter(client):
    """
    Test that custom timeout is applied to requests.
    """
    with patch.object(client.session, "get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"test": "data"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        client.get("/test", timeout=30)

        mock_get.assert_called_once()
        call_kwargs = mock_get.call_args.kwargs
        assert call_kwargs["timeout"] == 30


def test_timeout_on_all_http_methods(client):
    """
    Test that timeout is applied to all HTTP methods.
    """
    methods_and_params = [
        ("get", ["/"], {}),
        ("post", ["/", {}], {}),
        ("patch", ["/", {}], {}),
        ("put", ["/", {}], {}),
        ("delete", ["/"], {}),
    ]

    for method_name, args, kwargs in methods_and_params:
        with patch.object(client.session, method_name) as mock_method:
            mock_response = MagicMock()
            mock_response.json.return_value = {"test": "data"}
            mock_response.status_code = 200
            mock_method.return_value = mock_response

            method = getattr(client, method_name)
            method(*args, timeout=25, **kwargs)

            mock_method.assert_called_once()
            call_kwargs = mock_method.call_args.kwargs
            assert call_kwargs["timeout"] == 25


def test_connect_timeout_handling(client):
    """
    Test handling of connection timeout exceptions.
    """
    with patch.object(client.session, "get") as mock_get:
        mock_get.side_effect = ConnectTimeout("Connection timeout")

        with pytest.raises(ConnectTimeout):
            client.get("/")


def test_read_timeout_handling(client):
    """
    Test handling of read timeout exceptions.
    """
    with patch.object(client.session, "get") as mock_get:
        mock_get.side_effect = ReadTimeout("Read timeout")

        with pytest.raises(ReadTimeout):
            client.get("/")


@pytest.mark.parametrize("status_code", [404, 429, 500, 502, 503, 504])
def test_retry_on_server_errors(client, status_code):
    """
    Test that the client retries on server error status codes.
    """
    fake_conn = MagicMock()
    fake_conn.getresponse.side_effect = [
        MagicMock(status=status_code, msg=HTTPMessage()),
        MagicMock(status=status_code, msg=HTTPMessage()),
        MagicMock(status=status_code, msg=HTTPMessage()),
        MagicMock(status=200, msg=HTTPMessage()),
    ]

    with patch(
        "urllib3.connectionpool.HTTPConnectionPool._get_conn", return_value=fake_conn
    ), patch("urllib3.util.retry.Retry.sleep"):
        client.get("/")
        assert fake_conn.getresponse.call_count == 4


@pytest.mark.parametrize("status_code", [200, 201, 204])
def test_no_retry_on_successful_responses(client, status_code):
    """
    Test that successful responses (2xx) do not trigger retries.
    """
    fake_conn = MagicMock()
    fake_conn.getresponse.side_effect = [
        MagicMock(status=status_code, msg=HTTPMessage()),
    ]

    with patch(
        "urllib3.connectionpool.HTTPConnectionPool._get_conn", return_value=fake_conn
    ), patch("urllib3.util.retry.Retry.sleep"):
        client.get("/")
        assert fake_conn.getresponse.call_count == 1


def test_max_retries_exceeded(client):
    """
    Test that the client does not retry beyond the maximum retries set.
    """
    fake_conn = MagicMock()
    fake_conn.getresponse.side_effect = [
        MagicMock(status=500, msg=HTTPMessage()),
        MagicMock(status=500, msg=HTTPMessage()),
        MagicMock(status=500, msg=HTTPMessage()),
        MagicMock(status=500, msg=HTTPMessage()),
    ]

    with patch(
        "urllib3.connectionpool.HTTPConnectionPool._get_conn", return_value=fake_conn
    ), patch("urllib3.util.retry.Retry.sleep"):
        response = client.get("/")
        assert response["status_code"] == 500
        assert fake_conn.getresponse.call_count == 4
