from app.core.database.postgresql import Base
from sqlalchemy import Column, Integer, String, DateTime, Sequence
from sqlalchemy.orm import relationship

class Size(Base):
    __tablename__ = "sizes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    display_order = Column(Integer, Sequence('size_display_order_seq'), unique=True, nullable=False, server_default=Sequence('size_display_order_seq').next_value())
    product_sizes = relationship("ProductSize", back_populates="size")
