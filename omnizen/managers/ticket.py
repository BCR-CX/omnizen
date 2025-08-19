from omnizen.clients.async_client import AsyncZendeskAPIClient
from omnizen.clients.client import ZendeskAPIClient


class TicketManager:
    """
    Manages Zendesk tickets.
    """

    def __init__(
        self,
        *,
        client: ZendeskAPIClient | None = None,
        async_client: AsyncZendeskAPIClient | None = None,
    ):
        """
        Initializes the TicketManager with the given clients.
        """
        self._client = client or ZendeskAPIClient()
        self._async_client = async_client or AsyncZendeskAPIClient()

    def get_tickets(self, page: int = 1):
        """
        Retrieves tickets from Zendesk.
        """
        response = self._client.get("/tickets", params={"page": page})
        return response.json()

    async def get_tickets_async(self, page: int = 1, **kwargs):
        """
        Asynchronously retrieves tickets from Zendesk.
        """
        response = await self._async_client.get("/tickets", params={"page": page})
        return response.json()
