# services/crud.py
from decimal import Decimal
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from db.models import Product
from .session import get_session
from datetime import datetime, timezone
from db.models import PriceHistory

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

def update_product(
    product_id: int,
    *,
    name: Optional[str] = None,
    url: Optional[str] = None,
    target_price: Optional[float | Decimal | None] = ...,
) -> Product:
    """
    Update an existing product.
    - Pass target_price=... (ellipsis) to leave unchanged
    - Pass None to clear target_price
    """
    with get_session() as s:
        product = s.get(Product, product_id)
        if not product:
            raise ValueError(f"Product not found: id={product_id}")

        if name is not None:
            product.name = name.strip() if name else None

        if url is not None:
            new_url = url.strip()
            if not new_url:
                raise ValueError("URL cannot be empty")
            product.url = new_url

        if target_price is not ...:
            product.target_price = (
                Decimal(str(target_price)) if target_price is not None else None
            )

        s.flush()
        s.refresh(product)
        return product


def delete_product(product_id: int) -> None:
    """Delete a product from the wishlist."""
    with get_session() as s:
        product = s.get(Product, product_id)
        if not product:
            raise ValueError(f"Product not found: id={product_id}")
        s.delete(product)

def add_price_record(product_id: int, price: float | Decimal, note: Optional[str] = None) -> PriceHistory:
    """
    Add a new price entry linked to a product.
    """
    with get_session() as s:
        product = s.get(Product, product_id)
        if not product:
            raise ValueError(f"Product not found: id={product_id}")

        record = PriceHistory(
            product_id=product_id,
            price=float(price),
            note=note,
            recorded_at=datetime.now(timezone.utc),  # ✅ matches your model
        )
        s.add(record)
        s.flush()
        s.refresh(record)
        return record


def get_price_history(product_id: int) -> list[PriceHistory]:
    """
    Retrieve all price records for a product, newest first.
    """
    with get_session() as s:
        product = s.get(Product, product_id)
        if not product:
            raise ValueError(f"Product not found: id={product_id}")

        records = (
            s.query(PriceHistory)
            .filter(PriceHistory.product_id == product_id)
            .order_by(PriceHistory.recorded_at.desc())
            .all()
        )
        return records
