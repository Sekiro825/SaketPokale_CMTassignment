MEMBER_ENRICHMENT_PROMPT = """
You are an expert community manager and data analyst. Your task is to analyze the following member bio/comment and extract structured data.

Member Input:
"{bio}"

Please extraction the following:
1. Skills: A list of specific technical or soft skills mentioned or implied.
2. Persona: Classify the member into ONE of these categories: "Mentor Material", "Needs Guidance", "Passive", "Observer", "Contributor".
3. Confidence Score: A specific numeric score between 0.0 and 1.0 reflecting how confident you are in the extraction and classification based on the richness of the input. 1.0 is very confident, 0.0 is a guess.

Return the result as a valid JSON object matching the following schema:
{{
    "skills": ["string"],
    "persona": "string",
    "confidence_score": float
}}
"""
