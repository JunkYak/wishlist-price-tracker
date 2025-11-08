# scripts/test_dispatcher_detect.py

from _bootstrap import *
from scraper.dispatcher import identify_site

test_urls = [
    "https://www.amazon.in/dp/B0CHX1MPWG",
    "https://www.flipkart.com/apple-iphone-15/p/itm7b74c1c5e6e0a",
    "https://www.myntra.com/shoes",
    "https://www.ajio.com/men-tshirts",
    "https://www2.hm.com/en_in/productpage.123.html",
    "https://www.zara.com/in/en/jeans",
    "https://www.randomshop.io/product/123"
]

for url in test_urls:
    print(f"{url}  →  {identify_site(url)}")
