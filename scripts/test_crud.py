from _bootstrap import *
from services.crud import add_product, list_products, get_product_by_id

p = add_product("https://demo.com/itemY", name="Another Product", target_price=1200)
print("✅ Added:", p.id, p.name)

print("\n📦 All Products:")
for prod in list_products():
    print(prod.id, prod.name, prod.url)

pid = p.id
found = get_product_by_id(pid)
print(f"\n🔍 Found by ID {pid}: {found.name} ({found.url})")
