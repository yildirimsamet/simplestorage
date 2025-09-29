from app.core.database.postgresql import Base
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.sql import func

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    image = Column(String)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)