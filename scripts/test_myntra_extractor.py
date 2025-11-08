# scripts/test_myntra_extractor.py

from _bootstrap import *  # ✅ ensures imports work from project root
import asyncio

from scraper.browser import get_page, close_browser
from scraper.extractors.myntra import extract_product_details


TEST_URL = "https://www.myntra.com/tops/marks26spencer/marks--spencer-cut-out-detail-square-neck-puff-sleeves-top/25361316/buy"  # 🧪 example product URL


async def main():
    page = await get_page(TEST_URL)

    result = await extract_product_details(page)
    print("✅ Extraction Result:")
    print(result)

    # cleanup
    await page.context.close()
    await close_browser()


if __name__ == "__main__":
    asyncio.run(main())
