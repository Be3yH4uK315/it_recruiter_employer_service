from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app import crud, schemas
from app.core.db import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Employer, status_code=status.HTTP_201_CREATED)
def create_employer(employer: schemas.EmployerCreate, db: Session = Depends(get_db)):
    db_employer = crud.employer.get_employer_by_telegram_id(
        db, telegram_id=employer.telegram_id
    )
    if db_employer:
        return db_employer
    return crud.employer.create_employer(db=db, employer=employer)


@router.post("/{employer_id}/searches", response_model=schemas.SearchSession, status_code=status.HTTP_201_CREATED)
def create_search_session(employer_id: UUID, session: schemas.SearchSessionCreate, db: Session = Depends(get_db)):
    return crud.employer.create_employer_search_session(
        db=db, session=session, employer_id=employer_id
    )
