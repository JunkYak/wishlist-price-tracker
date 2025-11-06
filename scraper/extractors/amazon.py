# scraper/extractors/amazon.py

from playwright.async_api import Page

# ---------------------------------------
# Amazon Extractor — v1 (Playwright Locators)
# ---------------------------------------

async def extract_product_details(page: Page):
    """
    Extracts product name and price from an Amazon product page using Playwright locators.
    Returns: dict with 'name' and 'price'.
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
        ".a-price .a-offscreen",           # main price (discounted or final)
        "#priceblock_ourprice",            # old selector (some regions)
        "#priceblock_dealprice",           # deal price
        ".a-color-price"                   # fallback text
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
    
    print(f"[amazon] Extracted name: {name}")
    print(f"[amazon] Extracted price: {price}")


    return {
        "name": name,
        "price": price
    }


def _clean_price(price_str: str) -> float:
    """
    Cleans a price string like '₹2,499.00' or '$19.99' into a float (2499.00 or 19.99).
    """
    import re
    cleaned = re.sub(r"[^\d.,]", "", price_str)
    cleaned = cleaned.replace(",", "")
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

    return {
        "name": name,
        "price": price
    }
    