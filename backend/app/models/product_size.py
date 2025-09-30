from app.core.database.postgresql import Base
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class ProductSize(Base):
    __tablename__ = 'product_sizes'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    size_id = Column(Integer, ForeignKey('sizes.id', ondelete='RESTRICT'), nullable=False)
    price = Column(Float, nullable=False, default=0)
    stock = Column(Integer, nullable=False, default=0)
    product = relationship("Product", back_populates="product_sizes")
    size = relationship("Size", back_populates="product_sizes", lazy="selectin")

    __table_args__ = (
        UniqueConstraint('product_id', 'size_id', name="uq_product_size"),
    )