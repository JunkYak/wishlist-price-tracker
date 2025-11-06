# scripts/test_close_browser.py

from _bootstrap import *
import asyncio
from scraper.browser import launch_browser, close_browser

async def main():
    browser = await launch_browser()
    print("✅ Browser launched:", browser)
    await close_browser()
    print("🧹 Browser and Playwright closed cleanly.")

if __name__ == "__main__":
    asyncio.run(main())
