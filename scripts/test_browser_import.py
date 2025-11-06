# scripts/test_browser_import.py

from _bootstrap import *   # ✅ ensures we can import from project root

from scraper import browser

def test_imports():
    print("✅ Playwright imported successfully!")
    print("HEADLESS:", browser.HEADLESS)
    print("TIMEOUT:", browser.TIMEOUT)
    print("User agents loaded:", len(browser.USER_AGENTS))

if __name__ == "__main__":
    test_imports()
