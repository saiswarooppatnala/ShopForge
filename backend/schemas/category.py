from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    store_id: int


class CategoryUpdate(BaseModel):
    name: str | None = None
    store_id: int | None = None
