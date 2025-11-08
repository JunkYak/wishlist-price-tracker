# scripts/test_amazon_extractor.py

from _bootstrap import *
import asyncio
from scraper.browser import get_page, close_browser
from scraper.extractors.amazon import extract_product_details

TEST_URL = "https://www.amazon.in/Bath-Body-Works-Japanese-Fragrance/dp/B0DYJXHLTQ?crid=2QTXVTA341XZQ&dib=eyJ2IjoiMSJ9.1kB8guVTpjwmdtE-yqh-BfAGrG17W5aG9mR75ziZcvnyjT_xbZniZBB8F47RMEzOchJqxEtv3UF80-UytgfEI-DtnQO-dE_IBh6I6VCzLn8pJz2OeDItnO5XdJg7GUt_Cfv0WuNdX_GOpT56DBE5swMIPk3EZPLxyJd6wtXv9YawjNx72aVqUXv4q_9lazp6asvLV9mnffs745ZrGrWw6pyxfBDBjdJEEpozrKDCj_dbK651eK2An3QYyxegrmQm8fWJ9lvjbklBav-obnceQTYhNj30qtlr8-sDMpGJZ-Q.3nAh003vBYEX9Al8E9gjP1X_fAgSiCIZTzmoEJaRq_Q&dib_tag=se&keywords=bath+and+body+works+mist&qid=1762581428&sprefix=bath+and+body+works+mist%2Caps%2C277&sr=8-28"

async def main():
    page = await get_page(TEST_URL)
    data = await extract_product_details(page)
    print("✅ Extraction Result:")
    print(data)
    await page.context.close()
    await close_browser()

if __name__ == "__main__":
    asyncio.run(main())
