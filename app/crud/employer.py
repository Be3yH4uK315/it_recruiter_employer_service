from sqlalchemy.orm import Session
from uuid import UUID
from app import models, schemas
from sqlalchemy.dialects.postgresql import insert


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


# --- CRUD для Decision ---
def create_decision(db: Session, decision: schemas.DecisionCreate, session_id: UUID):
    stmt = insert(models.Decision).values(
        session_id=session_id,
        candidate_id=decision.candidate_id,
        decision=decision.decision,
        note=decision.note
    ).on_conflict_do_update(
        index_elements=['session_id', 'candidate_id'],
        set_={'decision': decision.decision, 'note': decision.note}
    ).returning(models.Decision)

    result = db.execute(stmt).scalar_one()
    db.commit()
    return result


# --- CRUD для ContactsRequest ---
def create_contact_request(db: Session, request: schemas.ContactsRequestCreate, employer_id: UUID, granted: bool):
    db_request = models.ContactsRequest(
        **request.model_dump(),
        employer_id=employer_id,
        granted=granted
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request