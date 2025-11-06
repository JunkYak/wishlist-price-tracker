# scraper/extractors/myntra.py

from playwright.async_api import Page

def _clean_price(text: str) -> float:
    """
    Converts price text like '₹5,000' to float 5000.0
    """
    if not text:
        return 0.0
    digits = "".join(ch for ch in text if ch.isdigit() or ch == ".")
    try:
        return float(digits)
    except ValueError:
        return 0.0

async def extract_product_details(page: Page) -> dict:
    """
    Extracts product name and price from a Myntra product page.
    Returns a dictionary: {"name": str, "price": float}
    """
    try:
        # Wait for the product title to appear
        await page.wait_for_selector("h1.pdp-name", timeout=10000)
        name = await page.locator("h1.pdp-name").inner_text()
        
        # Try to find the price within pdp-price block
        price = 0.0
        try:
            price_text = await page.locator("div.pdp-price strong").inner_text()
            price = _clean_price(price_text)
        except Exception:
            # fallback if structure differs
            price_text = await page.locator("strong").first.inner_text()
            price = _clean_price(price_text)

        print(f"[myntra] Extracted name: {name}")
        print(f"[myntra] Extracted price: {price}")

        return {"name": name.strip(), "price": price}

    except Exception as e:
        print(f"[myntra] ❌ Extraction failed: {e}")
        return {"name": "Unknown Product", "price": 0.0}
