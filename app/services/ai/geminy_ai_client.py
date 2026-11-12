from google import genai
from ...core.config import geminy_ai_settings

async def get_ai():
    client = genai.Client(api_key=geminy_ai_settings.geminy_api_key.get_secret_value()) 
    return client