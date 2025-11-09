from _bootstrap import *

import asyncio
from scraper.runner import scrape_product


# ------------------------------------------
# Test URLs — replace or extend freely
# ------------------------------------------
TEST_URLS = [
    "https://www.amazon.in/Bath-Body-Works-Japanese-Fragrance/dp/B0DYJXHLTQ",
    "https://www.flipkart.com/asics-gel-1130-casuals-men/p/itm0c4a8ea0f0364",
    "https://www.myntra.com/casual-shoes/asics/asics-gel-1130-unisex-leather-casual-sneakers/35128106/buy",
    "https://www.5feet11.com/collections/linen-pull-on-pants/products/blue-striped-cotton-pull-on-pants"
]

# Example email for per-user log path
USER_EMAIL = "ishan@gmail.com"


# ------------------------------------------
# Runner
# ------------------------------------------
async def main():
    print("🚀 Starting unified scraper test...\n")

    results = []
    for url in TEST_URLS:
        print(f"🔗 Testing: {url}\n")
        try:
            result = await scrape_product(url, user_email=USER_EMAIL)
            print(f"✅ Success → {result}\n")
            results.append(result)
        except Exception as e:
            print(f"❌ Failed for {url}: {e}\n")

    print("--- All Tests Complete ---")
    for r in results:
        print(r)


if __name__ == "__main__":
    asyncio.run(main())
