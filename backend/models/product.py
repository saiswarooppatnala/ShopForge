from sqlalchemy import Column, Integer, String, ForeignKey, Text
from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    cloudinary_public_id = Column(String, nullable=True)
    ai_category = Column(String, nullable=True)
    ai_tags = Column(String, nullable=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)