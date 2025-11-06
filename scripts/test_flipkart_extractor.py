from _bootstrap import *
import asyncio
from scraper.browser import get_page, close_browser
from scraper.extractors.flipkart import extract_product_details

TEST_URL = "https://www.flipkart.com/asics-gel-1130-casuals-men/p/itm0c4a8ea0f0364?pid=SHOH3BKMQK6BBTVZ&lid=LSTSHOH3BKMQK6BBTVZTJ3WMT&marketplace=FLIPKART&q=asics+gel+1130&store=osp%2Fcil&srno=s_1_2&otracker=search&otracker1=search&fm=Search&iid=05807a5b-b6fc-42bf-8c75-ed9b571ded0a.SHOH3BKMQK6BBTVZ.SEARCH&ppt=sp&ppn=sp&ssid=sz0ztxbcps0000001762449471972&qH=6d117c616e8c5f75"

async def main():
    page = await get_page(TEST_URL)
    data = await extract_product_details(page)
    print("✅ Extraction Result:")
    print(data)
    await page.context.close()
    await close_browser()

if __name__ == "__main__":
    asyncio.run(main())
