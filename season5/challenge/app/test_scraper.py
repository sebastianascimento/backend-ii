import asyncio
import aiohttp
import json

async def test_scraper():
    urls = [
        "https://example.com",
        "https://python.org",
        "https://fastapi.tiangolo.com"
    ]
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:8000/scrape/",
            json=urls
        ) as response:
            results = await response.json()
            print(json.dumps(results, indent=2))

if __name__ == "__main__":
    asyncio.run(test_scraper())