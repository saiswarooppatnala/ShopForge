from fastapi import FastAPI
from database import Base, engine
import models
from routes.store import router as store_router
from routes.user import router as user_router
from routes.category import router as category_router
from routes.product import router as product_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(store_router)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(product_router)


@app.get("/")
def home():
    return {"message": "ShopForge Backend is running"}