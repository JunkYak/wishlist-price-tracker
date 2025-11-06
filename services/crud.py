# services/crud.py
from decimal import Decimal
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from db.models import Product
from .session import get_session

def add_product(url: str, name: Optional[str] = None, target_price: Optional[float | Decimal] = None) -> Product:
    """
    Add a new product to the wishlist.
    Enforces unique URL constraint.
    """
    url = url.strip()
    if not url:
        raise ValueError("Product URL is required")

    with get_session() as s:
        new_product = Product(
            url=url,
            name=name.strip() if name else None,
            target_price=Decimal(str(target_price)) if target_price else None,
        )
        s.add(new_product)
        try:
            s.flush()
            s.refresh(new_product)
            # ✅ Detach before session closes (prevents DetachedInstanceError)
            s.expunge(new_product)
            return new_product
        except IntegrityError:
            s.rollback()
            raise ValueError(f"Product with this URL already exists: {url}")



def list_products() -> List[Product]:
    """Fetch all products sorted by latest first."""
    with get_session() as s:
        stmt = select(Product).order_by(Product.created_at.desc())
        products = list(s.scalars(stmt).all())
        # ✅ Detach each object so attributes stay accessible
        for p in products:
            s.expunge(p)
        return products



def get_product_by_id(product_id: int) -> Optional[Product]:
    """Fetch a single product by ID."""
    with get_session() as s:
        stmt = select(Product).where(Product.id == product_id)
        return s.scalars(stmt).first()
