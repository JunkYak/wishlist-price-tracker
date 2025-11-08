# scraper/extractors/amazon.py

from playwright.async_api import Page
import re

# ---------------------------------------
# Amazon Extractor — v2.2 (final availability tuning)
# ---------------------------------------

async def extract_product_details(page: Page):
    """
    Extracts product name, price, and availability from an Amazon product page using Playwright locators.
    Returns: dict with 'name', 'price', 'available'.
    """
    # Product title
    try:
        name_element = page.locator("#productTitle")
        name = (await name_element.inner_text()).strip()
    except Exception:
        name = "Unknown Product"

    # Product price
    price = None
    possible_selectors = [
        ".a-price .a-offscreen",
        "#priceblock_ourprice",
        "#priceblock_dealprice",
        ".a-color-price"
    ]

    for selector in possible_selectors:
        try:
            price_element = page.locator(selector)
            if await price_element.count() > 0:
                raw_price = (await price_element.first.inner_text()).strip()
                price = _clean_price(raw_price)
                break
        except Exception:
            continue

    if price is None:
        price = 0.0

   # ✅ Availability detection (final Amazon fix)
    available = True
    try:
        # Wait up to 5 seconds for the availability section to appear
        await page.wait_for_selector("#availability", timeout=5000)
        status_text = (await page.locator("#availability").inner_text()).strip().lower()
        if "currently unavailable" in status_text or "we don't know when" in status_text:
            available = False
    except Exception:
        pass



    print(f"[amazon] Extracted name: {name}")
    print(f"[amazon] Extracted price: {price}")
    print(f"[amazon] Availability: {'Available' if available else 'Currently Unavailable'}")

    
    

    return {
        "name": name,
        "price": price,
        "available": available,
    }

    # if unavailable, nullify price
    if not available:
        price = None



def _clean_price(price_str: str) -> float:
    """Cleans a price string like '₹2,499.00' or '$19.99' into a float."""
    cleaned = re.sub(r"[^\d.,]", "", price_str).replace(",", "")
    try:
        return float(cleaned)
    except ValueError:
        return 0.0
