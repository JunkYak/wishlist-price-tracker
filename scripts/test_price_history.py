from _bootstrap import *
from services.crud import add_price_record, get_price_history

pid = 2  # change to a real product ID that exists
add_price_record(pid, 1199.0, "Initial check")
add_price_record(pid, 999.0, "Sale price")

print(f"✅ Added price records for product {pid}")

for r in get_price_history(pid):
    print(f"{r.recorded_at} | ₹{r.price} | {r.note}")

