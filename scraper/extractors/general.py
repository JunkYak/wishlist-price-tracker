# scraper/extractors/general.py

async def extract_product_details(page):
    """
    Dummy fallback extractor for testing.
    Returns basic title and dummy price.
    """
    title = await page.title()
    return {
        "name": title,
        "price": 0.0
    }
