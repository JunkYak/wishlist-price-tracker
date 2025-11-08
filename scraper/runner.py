# scraper/runner.py
from scraper.dispatcher import extract_product_details

class ScrapeError(Exception):
    pass

async def scrape_product(url: str) -> dict:
    """
    Unified entry point that calls dispatcher.extract_product_details(),
    which dynamically imports the correct site extractor and runs it.
    Returns {name, price, source, url}.
    """
    try:
        result = await extract_product_details(url)

        # sanity validation
        if not result or not result.get("name") or not result.get("price"):
            raise ScrapeError(f"Incomplete data returned for {url}")

        return result

    except Exception as e:
        raise ScrapeError(f"Failed to scrape {url}: {e}") from e
