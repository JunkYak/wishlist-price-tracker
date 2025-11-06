# scraper/browser.py

import asyncio
import random
from playwright.async_api import async_playwright

# ---------------------------------------
# Configuration
# ---------------------------------------
HEADLESS = False  # Set to False to see browser
TIMEOUT = 15000  # 15 seconds
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/121.0",
]


# ---------------------------------------
# Browser State
# ---------------------------------------
_browser = None
_playwright = None

async def launch_browser():
    """
    Launch a single Playwright browser instance.
    This will be reused across all scraping sessions.
    """
    global _browser, _playwright

    # If browser already running, reuse it
    if _browser:
        print("[browser] Reusing existing browser instance.")
        return _browser

    # Start Playwright engine
    _playwright = await async_playwright().start()

    # Launch Chromium browser
    _browser = await _playwright.chromium.launch(headless=HEADLESS)
    print(f"[browser] Launched Chromium (headless={HEADLESS})")

    return _browser

async def get_page(url: str):
    """
    Opens a new browser page, navigates to the URL,
    and returns the loaded Playwright Page object.
    Includes timeout + retry safety.
    """
    browser = await launch_browser()

    # Create a new isolated browser context
    context = await browser.new_context(
        user_agent=random.choice(USER_AGENTS)
    )

    page = await context.new_page()

    try:
        print(f"[browser] Opening page: {url}")
        await page.goto(url, timeout=TIMEOUT)
        print("[browser] Page loaded successfully.")
        return page

    except Exception as e:
        print(f"[browser] ❌ Failed to load page: {e}")
        await context.close()
        raise

async def close_browser():
    """
    Gracefully closes the browser and Playwright engine.
    Prevents 'event loop closed' warnings during cleanup.
    """
    global _browser, _playwright

    try:
        if _browser:
            await _browser.close()
            print("[browser] Browser closed.")
            _browser = None

        if _playwright:
            await _playwright.stop()
            print("[browser] Playwright stopped.")
            _playwright = None

    except Exception as e:
        print(f"[browser] ⚠️ Error while closing browser: {e}")
