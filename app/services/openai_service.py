from openai import OpenAI
from app.utils.logging_config import logger
from config.settings import OPENAI_MODEL, OPENAI_API_KEY

class OpenAIService:
    def __init__(self):
        self.client = OpenAI()
        self.model = OPENAI_MODEL

    def generate_completion(self, system_prompt: str, user_prompt: str) -> tuple[str, bool]:
        """
        Generate a completion using OpenAI's API
        
        Args:
            system_prompt (str): The system prompt to set the context
            user_prompt (str): The user's prompt
            
        Returns:
            tuple[str, bool]: (response text, success status)
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content, True
        except Exception as e:
            logger.exception('OpenAI API error: %s', str(e))
            error_message = str(e)
            if "api_key" in error_message.lower():
                error_message = "OpenAI API key error. Please check your API key configuration."
            elif "rate limit" in error_message.lower():
                error_message = "Rate limit exceeded. Please try again in a moment."
            return error_message, False

# Create a singleton instance
openai_service = OpenAIService() 