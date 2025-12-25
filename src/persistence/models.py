from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Float, ForeignKey, Table, Column, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

# Many-to-Many association between Member and Skill
member_skill_association = Table(
    "member_skills",
    Base.metadata,
    Column("member_id", ForeignKey("members.id"), primary_key=True),
    Column("skill_id", ForeignKey("skills.id"), primary_key=True),
)

class Skill(Base):
    __tablename__ = "skills"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    
    # Relationship
    members: Mapped[List["Member"]] = relationship(
        secondary=member_skill_association, back_populates="skills"
    )

class Member(Base):
    __tablename__ = "members"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True) # Optional per CSV
    
    bio: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # Dates
    date_joined: Mapped[Optional[str]] = mapped_column(String, nullable=True) # ISO Date string
    last_activity: Mapped[Optional[str]] = mapped_column(String, nullable=True) # ISO Date string
    
    # Enrichment Data
    persona: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0)
    is_enriched: Mapped[bool] = mapped_column(default=False)
    
    # Metadata
    ingested_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    skills: Mapped[List["Skill"]] = relationship(
        secondary=member_skill_association, back_populates="members"
    )
