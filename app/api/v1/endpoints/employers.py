from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app import crud, schemas
from app.core.http_client import http_client
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


@router.post("/searches/{session_id}/decisions", response_model=schemas.Decision, status_code=status.HTTP_201_CREATED)
def create_decision_for_session(
    session_id: UUID,
    decision: schemas.DecisionCreate,
    db: Session = Depends(get_db)
):
    # Здесь нужна проверка, что сессия принадлежит текущему пользователю
    return crud.create_decision(db=db, decision=decision, session_id=session_id)


@router.post("/{employer_id}/contact-requests", response_model=schemas.ContactDetailsResponse)
async def request_candidate_contacts(
        employer_id: UUID,
        request: schemas.ContactsRequestCreate,
        db: Session = Depends(get_db)
):
    candidate_id = request.candidate_id
    candidate_profile = await http_client.get_candidate_profile(candidate_id)

    if not candidate_profile:
        raise HTTPException(status_code=404, detail="Candidate not found in Candidate Service")

    visibility = candidate_profile.get("contacts_visibility", "on_request")

    granted = False
    contacts = None

    if visibility == "public":
        granted = True
        contacts = candidate_profile.get("contacts")
    elif visibility == "on_request":
        granted = True
        contacts = candidate_profile.get("contacts")

    crud.create_contact_request(
        db=db, request=request, employer_id=employer_id, granted=granted
    )

    return schemas.ContactDetailsResponse(granted=granted, contacts=contacts)
