from _bootstrap import *
import asyncio
from scraper.browser import get_page, close_browser
from scraper.extractors.flipkart import extract_product_details

TEST_URL = "https://www.flipkart.com/asics-gel-1130-casuals-men/p/itmc8ffe859e874b?pid=SHOHCSKPHKSWHUSS&lid=LSTSHOHCSKPHKSWHUSSP2UYG2&marketplace=FLIPKART&q=asics+gel+1130&store=osp%2Fcil&srno=s_1_1&otracker=AS_Query_HistoryAutoSuggest_2_0&otracker1=AS_Query_HistoryAutoSuggest_2_0&fm=Search&iid=1c3e3c56-7474-4cd2-bdd6-e8fd4f6de8c3.SHOHCSKPHKSWHUSS.SEARCH&ppt=sp&ppn=sp&ssid=upgxjt2pow0000001762581721362&qH=6d117c616e8c5f75"

async def main():
    page = await get_page(TEST_URL)
    data = await extract_product_details(page)
    print("✅ Extraction Result:")
    print(data)
    await page.context.close()
    await close_browser()

if __name__ == "__main__":
    asyncio.run(main())



