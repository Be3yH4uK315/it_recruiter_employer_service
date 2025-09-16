from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from uuid import UUID
from app.models.employer import DecisionType

# --- EMPLOYER ---
class EmployerBase(BaseModel):
    company: Optional[str] = None
    contacts: Optional[dict] = None

class EmployerCreate(EmployerBase):
    telegram_id: int

class Employer(EmployerBase):
    id: UUID
    telegram_id: int

    class Config:
        from_attributes = True

# --- SEARCH ---
class SearchSessionBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    filters: Dict[str, Any]

class SearchSessionCreate(SearchSessionBase):
    pass

class SearchSession(SearchSessionBase):
    id: UUID
    employer_id: UUID

    class Confid:
        from_attributes = True

# --- DECIDION ---
class DecisionBase(BaseModel):
    candidate_id: UUID
    decision: DecisionType
    note: Optional[str] = None

class DecisionCreate(DecisionBase):
    pass

class Decision(DecisionBase):
    id: UUID
    session_id: UUID

    class Config:
        from_attributes = True

# --- CONTACTS ---
class ContactsRequestCreate(BaseModel):
    candidate_id: UUID

class ContactsRequest(ContactsRequestCreate):
    id: UUID
    employer_id: UUID
    granted: bool

    class Config:
        from_attributes = True

class ContactDetailsResponse(BaseModel):
    granted: bool
    contacts: Optional[Dict[str, Any]] = None