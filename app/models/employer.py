import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    String,
    Enum as SQLAlchemyEnum,
    DateTime,
    func,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID, BIGINT, JSONB
from app.core.db import Base
import enum


class SearchStatus(str, enum.Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    CLOSED = "closed"


class Employer(Base):
    __tablename__ = "employers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_id = Column(BIGINT, unique=True, index=True, nullable=False)
    company = Column(String(255), nullable=True)
    contacts = Column(JSONB)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    search_sessions = relationship(
        "SearchSession", back_populates="employer", cascade="all, delete-orphan"
    )


class SearchSession(Base):
    __tablename__ = "search_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employer_id = Column(UUID(as_uuid=True), ForeignKey("employers.id"), nullable=False)
    title = Column(String(255), nullable=False)
    filters = Column(JSONB, nullable=False)
    status = Column(
        SQLAlchemyEnum(SearchStatus), default=SearchStatus.ACTIVE, nullable=False
    )
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    employer = relationship("Employer", back_populates="search_sessions")
