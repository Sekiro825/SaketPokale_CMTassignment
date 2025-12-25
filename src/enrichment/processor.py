from typing import List, Dict, Any
from .llm_client import LLMClient
from .models import EnrichmentResult
from src.prompts import MEMBER_ENRICHMENT_PROMPT

class EnrichmentProcessor:
    def __init__(self):
        self.llm = LLMClient()

    def enrich_member(self, member_data: Dict[str, Any]) -> Dict[str, Any]:
        bio = member_data.get("bio", "")
        if not bio or len(bio) < 5:
            # Skip empty or too short bios
            return {
                **member_data,
                "skills": [],
                "persona": "Unknown",
                "confidence_score": 0.0,
                "enriched": False
            }

        prompt = MEMBER_ENRICHMENT_PROMPT.format(bio=bio)
        
        result_json = self.llm.generate_json(prompt)
        
        if result_json:
            try:
                # Validate with Pydantic
                enrichment = EnrichmentResult(**result_json)
                return {
                    **member_data,
                    "skills": enrichment.skills,
                    "persona": enrichment.persona,
                    "confidence_score": enrichment.confidence_score,
                    "enriched": True
                }
            except Exception as e:
                print(f"Validation Error for {member_data.get('full_name')}: {e}")
        
        return {
            **member_data,
            "skills": [],
            "persona": "Unknown",
            "confidence_score": 0.0,
            "enriched": False,
            "error": "LLM failed"
        }

    def process_batch(self, members: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        enriched_members = []
        for member in members:
            enriched = self.enrich_member(member)
            enriched_members.append(enriched)
        return enriched_members
