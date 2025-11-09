import json
from datetime import datetime
from scraper.dispatcher import extract_product_details
from scraper.utils import get_logger, retry_async, time_it


class ScrapeError(Exception):
    pass


@retry_async(retries=3, delay=2, backoff=2)
async def scrape_product(url: str, user_email: str | None = None) -> dict:
    """
    Unified orchestrator for product scraping.

    - Calls dispatcher to find and run the correct site extractor.
    - Measures duration and logs result to JSON (per user).
    - Retries failed scrapes up to 3 times with exponential backoff.

    Returns:
        dict: {
            "url": str,
            "source": str,
            "name": str,
            "price": float | None,
            "available": bool,
            "status": "success" | "failed",
            "attempts": int,
            "duration": str
        }
    """

    logger = get_logger(user_email)
    async with time_it() as t:
        start_time = datetime.now().isoformat()
        try:
            data = await extract_product_details(url)
            data["status"] = "success"
            data["attempts"] = 1  # handled by retry decorator context
            data["timestamp"] = start_time
            data["duration"] = f"{(t['duration'] or 0):.2f}s"


            # Write JSON log entry
            logger.info(json.dumps(data, ensure_ascii=False))
            return data

        except Exception as e:
            result = {
                "url": url,
                "status": "failed",
                "error": str(e),
                "timestamp": start_time,
                "duration": f"{(t['duration'] or 0):.2f}s",

            }
            logger.error(json.dumps(result, ensure_ascii=False))
            raise ScrapeError(f"Failed to scrape {url}: {e}") from e
