from pydantic import BaseModel, Field
from typing import List, Literal

class EnrichmentResult(BaseModel):
    skills: List[str] = Field(default_factory=list, description="List of extracted skills")
    persona: str = Field(..., description="Classified persona of the member")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score of the extraction")
