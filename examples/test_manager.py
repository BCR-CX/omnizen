import asyncio
import time
from dotenv import load_dotenv

from omnizen.clients.async_client import AsyncZendeskAPIClient
from omnizen.clients.client import ZendeskAPIClient
from omnizen.managers.ticket import TicketManager

load_dotenv()

manager = TicketManager(
    client=ZendeskAPIClient(
        api_token="APRRQD8fJrBhUW3XWfGrWOdX3kGLlFJ8DxrS23pW",
        domain="conbcrcx32481726685208",
        email="leonardo.guerra@bcrcx.com",
    ),
    async_client=AsyncZendeskAPIClient(
        api_token="APRRQD8fJrBhUW3XWfGrWOdX3kGLlFJ8DxrS23pW",
        domain="conbcrcx32481726685208",
        email="leonardo.guerra@bcrcx.com",
    ),
)

NUM_PAGES = 10


async def fetch_async():
    tasks = [manager.get_tickets_async(page=page) for page in range(1, NUM_PAGES + 1)]
    results = await asyncio.gather(*tasks)
    return results


def fetch_sync():
    results = []
    for page in range(1, NUM_PAGES + 1):
        res = manager.get_tickets(page=page)
        results.append(res)
    return results


async def main():
    # Async
    start_async = time.perf_counter()
    await fetch_async()
    end_async = time.perf_counter()
    async_time = end_async - start_async
    print(f"Async: {async_time:.2f} segundos")

    # Sync
    start_sync = time.perf_counter()
    fetch_sync()
    end_sync = time.perf_counter()
    sync_time = end_sync - start_sync
    print(f"Sync: {sync_time:.2f} segundos")

    print(
        f"Async é {sync_time - async_time:.2f} segundos mais rápido que Sync"
        if async_time < sync_time
        else f"Sync é {async_time - sync_time:.2f} segundos mais rápido que Async"
    )


if __name__ == "__main__":
    asyncio.run(main())
