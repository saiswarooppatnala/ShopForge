from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.category import Category
from models.store import Store
from schemas.category import CategoryCreate, CategoryUpdate
from auth import get_current_user


router = APIRouter()


@router.post("/categories")
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    store = db.query(Store).filter(
        Store.id == category_data.store_id,
        Store.owner_id == current_user
    ).first()

    if not store:
        return {"message": "Store not found"}

    category = Category(
        name=category_data.name,
        store_id=category_data.store_id
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


@router.get("/categories")
def get_categories(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    categories = db.query(Category).join(Store).filter(
        Store.owner_id == current_user
    ).all()

    return categories


@router.get("/categories/{category_id}")
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    category = db.query(Category).join(Store).filter(
        Category.id == category_id,
        Store.owner_id == current_user
    ).first()

    if not category:
        return {"message": "Category not found"}

    return category


@router.put("/categories/{category_id}")
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    category = db.query(Category).join(Store).filter(
        Category.id == category_id,
        Store.owner_id == current_user
    ).first()

    if not category:
        return {"message": "Category not found"}

    if category_data.name is not None:
        category.name = category_data.name

    if category_data.store_id is not None:
        new_store = db.query(Store).filter(
            Store.id == category_data.store_id,
            Store.owner_id == current_user
        ).first()

        if not new_store:
            return {"message": "Store not found"}

        category.store_id = category_data.store_id

    db.commit()
    db.refresh(category)

    return category


@router.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    category = db.query(Category).join(Store).filter(
        Category.id == category_id,
        Store.owner_id == current_user
    ).first()

    if not category:
        return {"message": "Category not found"}

    db.delete(category)
    db.commit()

    return {"message": "Category deleted successfully"}