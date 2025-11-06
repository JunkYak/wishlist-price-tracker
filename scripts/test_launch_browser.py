# scripts/test_launch_browser.py

from _bootstrap import *
import asyncio
from scraper.browser import launch_browser

async def main():
    browser = await launch_browser()
    print("✅ Browser object received:", browser)
    await browser.close()
    print("🧹 Browser closed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
