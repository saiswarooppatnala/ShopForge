from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.product import Product
from models.store import Store
from schemas.product import ProductCreate, ProductUpdate
from auth import get_current_user


router = APIRouter()


@router.post("/products")
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    store = db.query(Store).filter(
        Store.id == product_data.store_id,
        Store.owner_id == current_user
    ).first()

    if not store:
        return {"message": "Store not found"}

    product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        image_url=product_data.image_url,
        cloudinary_public_id=product_data.cloudinary_public_id,
        ai_category=product_data.ai_category,
        ai_tags=product_data.ai_tags,
        store_id=product_data.store_id,
        category_id=product_data.category_id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


@router.get("/products")
def get_products(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    products = db.query(Product).join(Store).filter(
        Store.owner_id == current_user
    ).all()

    return products


@router.get("/products/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    product = db.query(Product).join(Store).filter(
        Product.id == product_id,
        Store.owner_id == current_user
    ).first()

    if not product:
        return {"message": "Product not found"}

    return product


@router.put("/products/{product_id}")
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    product = db.query(Product).join(Store).filter(
        Product.id == product_id,
        Store.owner_id == current_user
    ).first()

    if not product:
        return {"message": "Product not found"}

    if product_data.name is not None:
        product.name = product_data.name

    if product_data.description is not None:
        product.description = product_data.description

    if product_data.price is not None:
        product.price = product_data.price

    if product_data.image_url is not None:
        product.image_url = product_data.image_url

    if product_data.cloudinary_public_id is not None:
        product.cloudinary_public_id = product_data.cloudinary_public_id

    if product_data.ai_category is not None:
        product.ai_category = product_data.ai_category

    if product_data.ai_tags is not None:
        product.ai_tags = product_data.ai_tags

    if product_data.category_id is not None:
        product.category_id = product_data.category_id

    db.commit()
    db.refresh(product)

    return product


@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    product = db.query(Product).join(Store).filter(
        Product.id == product_id,
        Store.owner_id == current_user
    ).first()

    if not product:
        return {"message": "Product not found"}

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}