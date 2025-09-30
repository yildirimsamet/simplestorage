from app.core.database.postgresql import Base
from sqlalchemy import Column, Integer, String, DateTime

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    