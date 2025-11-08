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
    Extracts product name, price, and availability from a Myntra product page.
    Returns a dictionary: {"name": str, "price": float or None, "available": bool}
    """
    try:
        # Wait for product title
        await page.wait_for_selector("h1.pdp-name", timeout=10000)
        name = await page.locator("h1.pdp-name").inner_text()
        
        # Try to extract price (may be missing if sold out)
        price = None
        try:
            price_text = await page.locator("div.pdp-price strong").inner_text()
            price = _clean_price(price_text)
        except Exception:
            try:
                price_text = await page.locator("strong").first.inner_text()
                price = _clean_price(price_text)
            except Exception:
                pass

        # ✅ Availability detection (from inspected snippet)
        available = True
        try:
            sold_out_el = page.locator(".size-buttons-out-of-stock, .pdp-out-of-stock")
            if await sold_out_el.count() > 0:
                texts = await sold_out_el.all_inner_texts()
                combined_text = " ".join(texts).lower()
                if "sold out" in combined_text or "out of stock" in combined_text:
                    available = False
        except Exception:
            pass

        # Nullify price if unavailable
        if not available:
            price = None

        print(f"[myntra] Extracted name: {name.strip()}")
        print(f"[myntra] Extracted price: {price}")
        print(f"[myntra] Availability: {'Available' if available else 'Sold Out'}")

        return {"name": name.strip(), "price": price, "available": available}

    except Exception as e:
        print(f"[myntra] ❌ Extraction failed: {e}")
        return {"name": "Unknown Product", "price": 0.0, "available": False}
