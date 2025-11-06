from _bootstrap import *
from services.crud import update_product, delete_product, list_products

# Update the latest product (adjust ID if needed)
updated = update_product(1, name="Updated Product", target_price=850)
print("✅ Updated:", updated.id, updated.name, updated.target_price)

# Show products after update
for p in list_products():
    print("📦", p.id, p.name, p.target_price)

# Delete same product
delete_product(1)
print("🗑️  Deleted product 1")

# Confirm deletion
for p in list_products():
    print("📦", p.id, p.name)
