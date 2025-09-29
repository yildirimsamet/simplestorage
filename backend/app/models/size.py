from app.core.database.postgresql import Base
from sqlalchemy import Column, Integer, String, DateTime

class Size(Base):
    __tablename__ = "sizes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    display_order = Column(Integer, unique=True, nullable=False)

