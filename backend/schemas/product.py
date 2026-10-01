from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    store_id: int
    description: str | None = None
    price: str | None = None
    image_url: str | None = None
    cloudinary_public_id: str | None = None
    ai_category: str | None = None
    ai_tags: str | None = None
    category_id: int | None = None


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: str | None = None
    image_url: str | None = None
    cloudinary_public_id: str | None = None
    ai_category: str | None = None
    ai_tags: str | None = None
    category_id: int | None = None
