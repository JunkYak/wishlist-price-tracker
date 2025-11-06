# scraper/browser.py

import asyncio
import random
from playwright.async_api import async_playwright

# ---------------------------------------
# Configuration
# ---------------------------------------
HEADLESS = True  # Set to False to see browser
TIMEOUT = 15000  # 15 seconds
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/121.0",
]
