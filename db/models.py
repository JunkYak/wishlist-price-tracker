# db/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, func
from sqlalchemy.orm import relationship
from .base import Base


# --------------------------
# Product table
# --------------------------
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(512), nullable=False)
    url = Column(String(2000), nullable=False, unique=True, index=True)
    notes = Column(Text, nullable=True)

    target_price = Column(Float, nullable=True)   # user-set desired price
    latest_price = Column(Float, nullable=True)   # most recently scraped price
    currency = Column(String(10), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # link to price history
    price_history = relationship(
        "PriceHistory",
        back_populates="product",
        cascade="all, delete-orphan",
        order_by="PriceHistory.recorded_at.desc()"
    )

    def __repr__(self):
        return f"<Product id={self.id} name={self.name!r} target={self.target_price}>"


# --------------------------
# PriceHistory table
# --------------------------
class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String(10), nullable=True)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    note = Column(String(255), nullable=True)

    product = relationship("Product", back_populates="price_history")

    def __repr__(self):
        return f"<PriceHistory id={self.id} product_id={self.product_id} price={self.price}>"
