# scripts/test_runner.py
from _bootstrap import *
import asyncio
from scraper.runner import scrape_product

async def main():
    urls = [
        "https://www.amazon.in/Bath-Body-Works-Japanese-Fragrance/dp/B0DYJXHLTQ?crid=36767523TEMQY&dib=eyJ2IjoiMSJ9.1kB8guVTpjwmdtE-yqh-BWFeyZuWShX-ruYo7O-ZOZKF1Mw1m78SgS4g0KguTkVuCycAI_-ukieEXUWvnfMyazMZXlobWCMyc6lBIpK5h_k5SDmhF7P4WlnWKOfysv9DwD9MsZMOL-2TOTtwKJlFRXJO4x7AupNvme_r-0XA9p8egL77ZGyWUPo7eTDsp869XfosvpIcopHJHk7ntbaELpR3P5ERyi5IiVnoXYd8E-rfU47OGIU3rNuN-8z88eyNGCLm6FRB1zRomq5fTAMbSzYhNj30qtlr8-sDMpGJZ-Q.44zkavZWCD-rxPfYahcZ7qyDbgZUfB3pD55WMdzNaWI&dib_tag=se&keywords=bath+and+body+works+mist&qid=1762427347&sprefix=batha+nd+%2Caps%2C263&sr=8-28",
        "https://www.flipkart.com/asics-gel-1130-casuals-men/p/itm0c4a8ea0f0364?pid=SHOH3BKMQK6BBTVZ&lid=LSTSHOH3BKMQK6BBTVZTJ3WMT&marketplace=FLIPKART&q=asics+gel+1130&store=osp%2Fcil&srno=s_1_2&otracker=search&otracker1=search&fm=Search&iid=05807a5b-b6fc-42bf-8c75-ed9b571ded0a.SHOH3BKMQK6BBTVZ.SEARCH&ppt=sp&ppn=sp&ssid=sz0ztxbcps0000001762449471972&qH=6d117c616e8c5f75",
        "https://www.myntra.com/casual-shoes/asics/asics-gel-1130-unisex-leather-casual-sneakers/35128106/buy",
    ]

    for url in urls:
        try:
            result = await scrape_product(url)
            print("✅", result)
        except Exception as e:
            print("❌", url, "→", e)

if __name__ == "__main__":
    asyncio.run(main())
