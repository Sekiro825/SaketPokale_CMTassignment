from src.persistence.database import init_db, get_db
from src.persistence.models import Member
import sys

# Ensure src is in path
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

init_db()
db = next(get_db())
members = db.query(Member).all()
print(f"Total Members: {len(members)}")
for m in members[:5]:
    print(f"Name: {m.full_name}, Score: {m.confidence_score}, Enriched: {m.is_enriched}, Bio: {m.bio[:30] if m.bio else 'None'}")
db.close()
