# scripts/test_engine.py
import sys, os
# add the project root (one level up from scripts/) to Python’s import path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db.base import engine

def main():
    print("DATABASE URL:", engine.url)
    with engine.connect() as conn:
        print("Connected — SQLAlchemy connection is open:", not conn.closed)
    print("Connection closed. Engine is ready.")

if __name__ == "__main__":
    main()
