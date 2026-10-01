from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.store import Store
from models.product import Product
from schemas.store import StoreCreate, StoreUpdate
from auth import get_current_user


router = APIRouter()


@router.post("/stores")
def create_store(
    store_data: StoreCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    store = Store(
        name=store_data.name,
        owner_id=current_user
    )

    db.add(store)
    db.commit()
    db.refresh(store)

    return store


@router.get("/stores")
def get_stores(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    stores = db.query(Store).filter(
        Store.owner_id == current_user
    ).all()

    return stores


@router.get("/stores/{store_id}")
def get_store(
    store_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    store = db.query(Store).filter(
        Store.id == store_id,
        Store.owner_id == current_user
    ).first()

    if not store:
        return {"message": "Store not found"}

    return store


@router.put("/stores/{store_id}")
def update_store(
    store_id: int,
    store_data: StoreUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    store = db.query(Store).filter(
        Store.id == store_id,
        Store.owner_id == current_user
    ).first()

    if not store:
        return {"message": "Store not found"}

    if store_data.name is not None:
        store.name = store_data.name

    db.commit()
    db.refresh(store)

    return store


@router.delete("/stores/{store_id}")
def delete_store(
    store_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    store = db.query(Store).filter(
        Store.id == store_id,
        Store.owner_id == current_user
    ).first()

    if not store:
        return {"message": "Store not found"}

    db.delete(store)
    db.commit()

    return {"message": "Store deleted successfully"}


@router.get("/stores/{store_id}/catalog")
def get_store_catalog(
    store_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    store = db.query(Store).filter(
        Store.id == store_id,
        Store.owner_id == current_user
    ).first()

    if not store:
        return {"message": "Store not found"}

    products = db.query(Product).filter(
        Product.store_id == store_id
    ).all()

    return products