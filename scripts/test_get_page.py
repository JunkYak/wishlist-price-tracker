# scripts/test_get_page.py

from _bootstrap import *
import asyncio
from scraper.browser import get_page

TEST_URL = "https://www.amazon.in/Bath-Body-Works-Japanese-Fragrance/dp/B0DYJXHLTQ?crid=36767523TEMQY&dib=eyJ2IjoiMSJ9.1kB8guVTpjwmdtE-yqh-BWFeyZuWShX-ruYo7O-ZOZKF1Mw1m78SgS4g0KguTkVuCycAI_-ukieEXUWvnfMyazMZXlobWCMyc6lBIpK5h_k5SDmhF7P4WlnWKOfysv9DwD9MsZMOL-2TOTtwKJlFRXJO4x7AupNvme_r-0XA9p8egL77ZGyWUPo7eTDsp869XfosvpIcopHJHk7ntbaELpR3P5ERyi5IiVnoXYd8E-rfU47OGIU3rNuN-8z88eyNGCLm6FRB1zRomq5fTAMbSzYhNj30qtlr8-sDMpGJZ-Q.44zkavZWCD-rxPfYahcZ7qyDbgZUfB3pD55WMdzNaWI&dib_tag=se&keywords=bath+and+body+works+mist&qid=1762427347&sprefix=batha+nd+%2Caps%2C263&sr=8-28"

async def main():
    page = await get_page(TEST_URL)
    html = await page.content()
    print(f"✅ Loaded {TEST_URL} | HTML length: {len(html)}")

    # Close the page and its context after test
    await page.context.close()
    print("🧹 Page and context closed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
