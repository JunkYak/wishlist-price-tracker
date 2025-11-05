# scripts/test_models.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # add project root

from db.base import Base, engine, SessionLocal
from db.models import Product, PriceHistory

def main():
    print("Creating tables if not exist...")
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    # --- Check if product already exists ---
    existing = session.query(Product).filter_by(url="https://example.com/sony-wh1000xm5").first()
    if existing:
        print("Product already exists, skipping insert:", existing)
        product = existing
    else:
        # --- Add a new sample product ---
        product = Product(
            name="Sony WH-1000XM5",
            url="https://example.com/sony-wh1000xm5",
            target_price=25000.0,
            currency="INR"
        )
        session.add(product)
        session.commit()
        session.refresh(product)
        print("Inserted product:", product)

    # --- Add a sample price history record ---
    price_entry = PriceHistory(product_id=product.id, price=24999.0, note="test run")
    session.add(price_entry)
    session.commit()
    session.refresh(price_entry)
    print("Inserted price record:", price_entry)

    # --- Query back ---
    products = session.query(Product).all()
    for p in products:
        print(f"{p.name} has {len(p.price_history)} price records.")
        for ph in p.price_history:
            print("   ", ph)

    session.close()

if __name__ == "__main__":
    main()
