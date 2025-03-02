import os
from dotenv import load_dotenv

load_dotenv()

# Flask Configuration
FLASK_DEBUG = os.getenv('FLASK_DEBUG', True)
FLASK_PORT = int(os.getenv('FLASK_PORT', 5001))

# CORS Configuration
CORS_ORIGINS = [
    "http://127.0.0.1:5001",
    "http://localhost:5001",
    "http://freepmtools.com",
    "https://freepmtools.com"
]
CORS_METHODS = ["GET", "POST", "OPTIONS"]
CORS_HEADERS = ["Content-Type"]

# OpenAI Configuration
OPENAI_MODEL = "gpt-4o-mini"  # Updated to the new model name as per instructions
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG') 