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
    Extracts product name, price, and availability from a Flipkart product page.
    Returns: dict with 'name', 'price', 'available'.
    """
    try:
        # Wait for title element
        await page.wait_for_selector("span.VU-ZEz", timeout=15000)
        name_el = page.locator("span.VU-ZEz")
        name = (await name_el.inner_text()).strip()

        # Try to get price (may not exist if sold out)
        price = None
        try:
            price_el = page.locator("div.Nx9bqj.CxhGGd")
            if await price_el.count() > 0:
                raw_price = (await price_el.first.inner_text()).strip()
                price = _clean_price(raw_price)
        except Exception:
            pass

        # ✅ Availability detection using your confirmed selectors
        available = True
        try:
            sold_out_el = page.locator("div.Z8JjpR, div.nbiUlm")
            if await sold_out_el.count() > 0:
                text = (await sold_out_el.all_inner_texts())
                text = " ".join(text).lower()
                if "sold out" in text or "out of stock" in text:
                    available = False
        except Exception:
            pass

        # Nullify price if unavailable
        if not available:
            price = None

        print(f"[flipkart] Extracted name: {name}")
        print(f"[flipkart] Extracted price: {price}")
        print(f"[flipkart] Availability: {'Available' if available else 'Sold Out'}")

        return {"name": name, "price": price, "available": available}

    except Exception as e:
        print(f"[flipkart] ❌ Extraction failed: {e}")
        return {"name": "Unknown Product", "price": 0.0, "available": False}

