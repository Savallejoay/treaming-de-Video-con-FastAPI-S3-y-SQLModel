from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from db import engine
from models import Category
from typing import List

router = APIRouter()

@router.get("/categories", response_model=List[Category])
def get_categories():
    with Session(engine) as session:
        categories = session.exec(select(Category)).all()
        return categories

@router.post("/categories", response_model=Category)
def create_category(category: Category):
    with Session(engine) as session:
        if not category.name or not category.name.strip():
            raise HTTPException(status_code=400, detail="El nombre de la categoría no puede estar vacío")
        existing_category = session.exec(
            select(Category).where(Category.name == category.name.strip())
        ).first()
        if existing_category:
            raise HTTPException(status_code=400, detail="Esta categoría ya existe")

        category.id = None
        category.name = category.name.strip()
        
        session.add(category)
        session.commit()
        session.refresh(category)

        return category