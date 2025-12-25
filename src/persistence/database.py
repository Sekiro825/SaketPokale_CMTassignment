from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base, Member, Skill
import os

DB_URL = "sqlite:///volunteer_data.db"

engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Creates tables if they don't exist."""
    print(f"Initializing database at {DB_URL}")
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_enriched_data(session: Session, enriched_records: list[dict]):
    """
    Saves enriched records to DB, handling deduplication and skill normalization.
    Algorithm:
    1. Check if member exists (by name? email missing in some). 
       Using Name + Bio hash or just Name if unique?
       Prompt says "Versioning... or idempotent".
       Let's assume Name is unique enough for this exercise or update existing.
    2. Create/Update Member.
    3. Resolve Skills (get or create).
    4. Link Skills.
    """
    
    # Pre-fetch all skills to avoid unique constraint errors in the same batch
    existing_skills = session.query(Skill).all()
    skill_map = {s.name: s for s in existing_skills}

    for record in enriched_records:
        # 1. Find or Create Member
        # Strategy: Match by Full Name (imperfect but required given data)
        name = record.get("full_name")
        if not name:
            continue
            
        member = session.query(Member).filter(Member.full_name == name).first()
        if not member:
            member = Member(full_name=name)
            session.add(member)
            # Flush to get ID if needed, but we can set attrs
        
        # Update attributes
        member.email = record.get("email")
        member.date_joined = record.get("date_joined")
        member.last_activity = record.get("last_activity")
        member.bio = record.get("bio")
        member.persona = record.get("persona")
        member.confidence_score = record.get("confidence_score", 0.0)
        member.is_enriched = record.get("enriched", False)
        # ingested_at updates on insert, preserve generic
        
        # 2. Handle Skills
        skill_names = record.get("skills", [])
        current_skills = []
        for s_name in skill_names:
            s_name = s_name.strip().lower() # Normalize skill name
            if not s_name:
                continue
                
            if s_name in skill_map:
                skill = skill_map[s_name]
            else:
                skill = Skill(name=s_name)
                session.add(skill)
                # Add to map immediately so next occurrence in this loop finds it
                skill_map[s_name] = skill
            
            if skill not in current_skills:
                current_skills.append(skill)
        
        member.skills = current_skills # Update relationship
        
    session.commit()
