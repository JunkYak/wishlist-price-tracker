# init_db.py
from db.base import Base, engine
from db.models import Product, PriceHistory
from sqlalchemy import inspect


def init_database():
    """
    Creates all tables if they don't exist and verifies the schema.
    Can be run safely multiple times.
    """
    print("🔧 Creating database tables if not present...")
    Base.metadata.create_all(bind=engine)

    # Use SQLAlchemy inspector to list all tables in the connected DB
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    print("\n✅ Tables present in database:")
    for t in tables:
        print("   •", t)

    # Validate that required tables exist
    expected = {"products", "price_history"}
    missing = expected - set(tables)

    if missing:
        print("\n⚠️ Missing expected tables:", missing)
    else:
        print("\n🎉 Database initialization successful — all tables created and verified.")


if __name__ == "__main__":
    init_database()
    