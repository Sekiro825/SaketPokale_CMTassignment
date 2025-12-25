import os
import json
import logging
from typing import Optional, Dict, Any
from .models import EnrichmentResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = None
        self.mock_mode = False

        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found. Running in MOCK mode.")
            self.mock_mode = True
        else:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.client = genai.GenerativeModel('gemini-pro')
            except ImportError:
                logger.error("google-generativeai not installed. Running in MOCK mode.")
                self.mock_mode = True

    def generate_json(self, prompt: str) -> Optional[Dict[str, Any]]:
        if self.mock_mode:
            return self._mock_response()

        try:
            response = self.client.generate_content(prompt)
            # Gemini doesn't always return pure JSON, we might need to strip markdown
            text = response.text
            clean_text = text.replace('```json', '').replace('```', '').strip()
            return json.loads(clean_text)
        except Exception as e:
            logger.error(f"LLM Generation Error: {e}")
            return None

    def _mock_response(self) -> Dict[str, Any]:
        return {
            "skills": ["Mock Skill 1", "Python"],
            "persona": "Observer",
            "confidence_score": 0.5
        }
