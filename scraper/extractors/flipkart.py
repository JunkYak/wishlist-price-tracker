# scraper/extractors/flipkart.py

from playwright.async_api import Page

# ---------------------------------------
# Flipkart Extractor — v2 (Updated Selectors)
# ---------------------------------------

def _clean_price(price_str: str) -> float:
    """Convert a string like '₹4,319' to 4319.0"""
    import re
    cleaned = re.sub(r"[^\d.,]", "", price_str)
    cleaned = cleaned.replace(",", "")
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


async def extract_product_details(page: Page):
    """
    Extracts product name and price from a Flipkart product page.
    Returns: dict with 'name' and 'price'.
    """
    try:
        # Wait for title and price elements
        await page.wait_for_selector("span.VU-ZEz", timeout=15000)
        await page.wait_for_selector("div.Nx9bqj.CxhGGd", timeout=15000)

        # Extract product name
        name_el = page.locator("span.VU-ZEz")
        name = (await name_el.inner_text()).strip()

        # Extract product price
        price_el = page.locator("div.Nx9bqj.CxhGGd")
        price_raw = (await price_el.first.inner_text()).strip()
        price = _clean_price(price_raw)

        print(f"[flipkart] Extracted name: {name}")
        print(f"[flipkart] Extracted price: {price}")

        return {"name": name, "price": price}

    except Exception as e:
        print(f"[flipkart] ❌ Extraction failed: {e}")
        return {"name": "Unknown Product", "price": 0.0}
