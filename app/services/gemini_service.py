import google.generativeai as genai
from PIL import Image
from app.config import settings
import logging

logger = logging.getLogger("shelf-scanner-backend")

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    async def analyze_shelf(self, image: Image.Image, preferences: str) -> str:
        try:
            # Crafting a precise prompt to force structural outputs
            prompt = (
                f"You are an expert librarian and AI book recommender. "
                f"1. Analyze this image and extract all visible book titles and authors.\n"
                f"2. Based on the books you found and the user's explicit preference: '{preferences}', "
                f"recommend the top 3 best matching books visible on the shelf.\n"
                f"3. Give a clear, 2-sentence explanation for each recommendation explaining why it fits their interest."
            )
            
            # Sending both the raw optimized image and the text prompt to Gemini
            response = self.model.generate_content([prompt, image])
            return response.text
            
        except Exception as e:
            logger.error(f"Failed to communicate with Gemini API: {str(e)}")
            raise RuntimeError("Gemini API processing failed.")