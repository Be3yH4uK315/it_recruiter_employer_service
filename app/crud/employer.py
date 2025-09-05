from sqlalchemy.orm import Session
from uuid import UUID
from app import models, schemas


# --- CRUD для Employer ---
def get_employer_by_telegram_id(db: Session, telegram_id: int):
    return (
        db.query(models.Employer)
        .filter(models.Employer.telegram_id == telegram_id)
        .first()
    )


def create_employer(db: Session, employer: schemas.EmployerCreate):
    db_employer = models.Employer(**employer.model_dump())
    db.add(db_employer)
    db.commit()
    db.refresh(db_employer)
    return db_employer


# --- CRUD для SearchSession ---
def create_employer_search_session(
    db: Session, session: schemas.SearchSessionCreate, employer_id: UUID
):
    db_session = models.SearchSession(**session.model_dump(), employer_id=employer_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session
