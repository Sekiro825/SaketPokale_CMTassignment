import streamlit as st
import pandas as pd
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from sqlalchemy.orm import Session
from src.persistence.database import get_db, init_db
from src.persistence.models import Member, Skill

st.set_page_config(page_title="Volunteer-First OS", layout="wide")

st.title("Saket Pokale:Volunteer-First OS- Shadow Source of Truth")

# Initialize DB connection
try:
    init_db()
    db = next(get_db())
except Exception as e:
    st.error(f"Database Error: {e}")
    st.stop()

# Sidebar Filters
st.sidebar.header("Filter & Rank")

search_query = st.sidebar.text_input("Search (Name/Bio/Location)", help="e.g. Mumbai")
selected_persona = st.sidebar.multiselect(
    "Persona", 
    ["Mentor Material", "Needs Guidance", "Passive", "Observer", "Contributor", "Unknown"]
)
min_confidence = st.sidebar.slider("Min Confidence Score", 0.0, 1.0, 0.5)

sort_by = st.sidebar.selectbox("Sort By", ["Confidence Score", "Last Activity", "Name"])

# Query Logic
query = db.query(Member)

if search_query:
    search = f"%{search_query}%"
    query = query.filter(
        (Member.full_name.ilike(search)) | 
        (Member.bio.ilike(search))
    )

if selected_persona:
    query = query.filter(Member.persona.in_(selected_persona))

query = query.filter(Member.confidence_score >= min_confidence)

# Sorting
if sort_by == "Confidence Score":
    query = query.order_by(Member.confidence_score.desc())
elif sort_by == "Last Activity":
    query = query.order_by(Member.last_activity.desc().nullslast())
elif sort_by == "Name":
    query = query.order_by(Member.full_name)

results = query.all()

st.subheader(f"Results: {len(results)} members found")

if not results:
    st.info("No members found matching criteria.")
else:
    data = []
    for m in results:
        skills = ", ".join([s.name for s in m.skills])
        data.append({
            "Name": m.full_name,
            "Persona": m.persona,
            "Score": round(m.confidence_score, 2),
            "Skills": skills,
            "Last Activity": m.last_activity,
            "Bio": m.bio # Truncate in UI?
        })
    
    df = pd.DataFrame(data)
    # Display as interactive table
    st.dataframe(
        df, 
        column_config={
            "Score": st.column_config.ProgressColumn(
                "Confidence",
                help="AI Confidence Score",
                format="%.2f",
                min_value=0,
                max_value=1,
            ),
        },
        use_container_width=True
    )

    with st.expander("View Raw Data for Top Result"):
        st.json({
            "name": results[0].full_name,
            "email": results[0].email,
            "skills": [s.name for s in results[0].skills],
            "raw_bio": results[0].bio
        })
