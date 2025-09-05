from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from uuid import UUID


# --- Схемы для Employer ---
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


# --- Схемы для SearchSession ---
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
