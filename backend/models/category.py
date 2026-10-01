from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)