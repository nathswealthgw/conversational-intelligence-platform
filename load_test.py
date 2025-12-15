import asyncio
import time

import httpx


async def run_load_test(concurrency: int = 25, duration: int = 10) -> None:
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        start = time.time()
        requests = 0
        while time.time() - start < duration:
            tasks = [
                client.post(
                    "/api/v1/chat/ask",
                    json={
                        "conversation_id": "load",
                        "question": "Summarize retention risks.",
                        "top_k": 3,
                    },
                )
                for _ in range(concurrency)
            ]
            await asyncio.gather(*tasks)
            requests += concurrency
        elapsed = time.time() - start
        print(f"Executed {requests} requests in {elapsed:.2f}s")


if __name__ == "__main__":
    asyncio.run(run_load_test())
