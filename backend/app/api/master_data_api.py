from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.entities import Facility, Product, Supplier, RouteMaster

router = APIRouter(tags=["Master Data"])

@router.get("/facilities")
def get_facilities(db: Session = Depends(get_db)):
    return db.query(Facility).all()

@router.get("/facilities/{facility_id}")
def get_facility_by_id(facility_id: str, db: Session = Depends(get_db)):
    fac = db.query(Facility).filter_by(facility_id=facility_id).first()
    if not fac:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Facility not found")
    return fac

@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.get("/suppliers")
def get_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).all()

@router.get("/routes")
def get_routes(db: Session = Depends(get_db)):
    return db.query(RouteMaster).all()
