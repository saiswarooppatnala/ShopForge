from pydantic import BaseModel


class StoreCreate(BaseModel):
    name: str


class StoreUpdate(BaseModel):
    name: str | None = None