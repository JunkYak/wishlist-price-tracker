# scraper/extractors/general.py

from playwright.async_api import Page
from bs4 import BeautifulSoup
import re


async def extract_product_details(page: Page):
    """
    Generic fallback extractor for unknown e-commerce sites.
    Uses HTML parsing heuristics to detect title, price, and availability.
    Returns a safe structured dict: {"name": str, "price": float or None, "available": bool}
    """
    try:
        # get HTML and parse with BeautifulSoup
        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")

        # ---------- 1. product name ----------
        name = None
        if soup.title and soup.title.text.strip():
            name = soup.title.text.strip()
        elif soup.find("h1"):
            name = soup.find("h1").get_text(strip=True)
        elif soup.find("meta", property="og:title"):
            name = soup.find("meta", property="og:title")["content"]
        else:
            name = "Unknown Product"

        # ---------- 2. advanced price extraction (universal + Shopify tested) ----------
        price = None
        price_candidates = []

        # (a) direct numeric text with or without currency
        for tag in soup.find_all(string=re.compile(r"(₹|Rs\.|INR|\$|€)?\s*\d[\d,]*(?:\.\d{1,2})?")):
            price_candidates.append(tag.strip())

        # (b) any element with price/amount class or id
        for tag in soup.find_all(attrs={"class": re.compile("price|amount", re.I)}):
            text = tag.get_text(strip=True)
            if re.search(r"\d", text):
                price_candidates.append(text)

        # (c) itemprop or content-based prices (Shopify, meta, schema.org)
        for tag in soup.find_all(["span", "meta", "div"], attrs={"itemprop": re.compile("price", re.I)}):
            if tag.get("content"):
                price_candidates.append(tag["content"])
            elif tag.get("data-price"):
                price_candidates.append(tag["data-price"])
            elif tag.get("data-product-price"):
                price_candidates.append(tag["data-product-price"])
            else:
                text = tag.get_text(strip=True)
                if re.search(r"\d", text):
                    price_candidates.append(text)

        # (d) Shopify-specific explicit selector
        for tag in soup.select("span.js-product-price, span.product-single__price"):
            text = tag.get_text(strip=True)
            if re.search(r"\d", text):
                price_candidates.append(text)
            if tag.get("content"):
                price_candidates.append(tag["content"])

        # clean & parse
        if price_candidates:
            # Pick the most likely valid candidate (last one usually visible)
            raw = str(price_candidates[-1])
            clean = re.sub(r"[^\d.]", "", raw)
            try:
                price = float(clean)
            except ValueError:
                price = None

        # ---------- 3. refined availability detection ----------
        available = True
        availability_texts = []

        # Look for elements likely describing stock state
        for tag in soup.find_all(["div", "span", "p"], attrs={"class": re.compile("stock|availability", re.I)}):
            availability_texts.append(tag.get_text(strip=True).lower())

        # fallback to empty string join if nothing found
        joined_text = " ".join(availability_texts)
        if any(kw in joined_text for kw in ["out of stock", "sold out", "unavailable", "not available"]):
            available = False
            price = None

        # ---------- 4. log + return ----------
        print(f"[general] Extracted name: {name}")
        print(f"[general] Extracted price: {price}")
        print(f"[general] Availability: {'Available' if available else 'Unavailable'}")

        return {
            "name": name,
            "price": price,
            "available": available,
        }

    except Exception as e:
        print(f"[general] ❌ Extraction failed: {e}")
        return {
            "name": "Unknown Product",
            "price": None,
            "available": False,
        }
