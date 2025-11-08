# scraper/dispatcher.py

import re
import importlib
from scraper.browser import get_page, close_browser

# ---------------------------------------
# Site Detection
# ---------------------------------------

def identify_site(url: str) -> str:
    """
    Detects which supported e-commerce site the URL belongs to.
    Returns one of: 'amazon', 'flipkart', 'myntra', 'ajio', 'hm', 'zara', or 'general'.
    """
    url = url.lower()

    if "amazon." in url:
        return "amazon"
    elif "flipkart." in url:
        return "flipkart"
    elif "myntra." in url:
        return "myntra"
    elif "ajio." in url:
        return "ajio"
    elif "hm.com" in url or "h&m" in url:
        return "hm"
    elif "zara.com" in url:
        return "zara"
    else:
        return "general"



# ---------------------------------------
# Dynamic Routing to Extractors
# ---------------------------------------

async def extract_product_details(url: str):
    """
    Routes a product URL to the correct site-specific extractor.
    Returns a dictionary: {source, name, price, url}
    """
    site = identify_site(url)
    print(f"[dispatcher] Detected site: {site}")

    try:
        # Try to import the site-specific extractor dynamically
        module_path = f"scraper.extractors.{site}"
        extractor = importlib.import_module(module_path)
    except ModuleNotFoundError:
        print(f"[dispatcher] ⚠️ Extractor for '{site}' not found, using 'general'")
        from scraper.extractors import general as extractor

    # Load the page and pass it to the extractor
    page = await get_page(url)

    try:
        data = await extractor.extract_product_details(page)
        data["source"] = site
        data["url"] = url
    finally:
        await page.context.close()

    return data

