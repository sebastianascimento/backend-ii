from fastapi import FastAPI, HTTPException
import asyncio
import aiohttp
from typing import List, Dict, Any

app = FastAPI(
    title="Async Web Scraper API",
    description="API that fetches HTML content from multiple URLs concurrently"
)

async def fetch_url(session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
    """Fetch HTML content from a URL asynchronously."""
    try:
        # Use a timeout to prevent hanging on slow websites
        async with session.get(url, timeout=10) as response:
            content = await response.text()
            return {
                "url": url,
                "status": response.status,
                "content_length": len(content),
                "content": content[:500] + "..." if len(content) > 500 else content,  # Truncate for display
                "headers": dict(response.headers)
            }
    except asyncio.TimeoutError:
        return {"url": url, "error": "Request timed out"}
    except aiohttp.ClientError as e:
        return {"url": url, "error": f"Client error: {str(e)}"}
    except Exception as e:
        return {"url": url, "error": f"Unexpected error: {str(e)}"}

@app.post("/scrape/", response_model=List[Dict[str, Any]])
async def scrape_urls(urls: List[str]):
    """
    Fetch HTML content from multiple URLs concurrently.
    
    - **urls**: List of URLs to scrape
    
    Returns a list of dictionaries containing URL, status code, content length, 
    headers, and a preview of the content (or error message if request failed).
    """
    if not urls:
        raise HTTPException(status_code=400, detail="No URLs provided")
        
    # Limit the number of URLs to prevent abuse
    if len(urls) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 URLs allowed per request")
        
    # Create a single session for all requests
    async with aiohttp.ClientSession() as session:
        # Use asyncio.gather to fetch all URLs concurrently
        results = await asyncio.gather(
            *[fetch_url(session, url) for url in urls]
        )
        
    return results

# Health check endpoint
@app.get("/", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Async Web Scraper API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.async_scraper:app", host="0.0.0.0", port=8000, reload=True)