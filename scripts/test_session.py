# scripts/test_session.py
from _bootstrap import *   # ✅ ensures we can import from project root

from db.models import Product
from services.session import get_session

with get_session() as s:
    p = Product(url="https://demo.com/item1", name="Demo Item", target_price=1000)
    s.add(p)
    print("✅ Added product, will auto-commit when this block ends")

with get_session() as s:
    products = s.query(Product).all()
    print("📦 All Products:")
    for prod in products:
        print(f"ID={prod.id} | Name={prod.name} | URL={prod.url}")
