from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import WasteInferenceLog, WasteCategory
from app.schemas import WasteLogCreate, WasteCategoryCreate

router = APIRouter()

@router.post("/waste", status_code=201)
def create_waste_log(waste_log: WasteLogCreate, db: Session = Depends(get_db)):
    waste_entry = WasteInferenceLog(**waste_log.dict())
    db.add(waste_entry)
    db.commit()
    db.refresh(waste_entry)
    return waste_entry

@router.get("/waste", status_code=200)
def get_waste_logs(db: Session = Depends(get_db)):
    return db.query(WasteInferenceLog).all()

@router.post("/category", status_code=201)
def create_waste_category(category: WasteCategoryCreate, db: Session = Depends(get_db)):
    new_category = WasteCategory(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/category", status_code=200)
def get_waste_categories(db: Session = Depends(get_db)):
    return db.query(WasteCategory).all()