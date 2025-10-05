import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # WhatsApp Business API
    WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
    WHATSAPP_VERIFY_TOKEN = os.getenv('WHATSAPP_VERIFY_TOKEN')
    WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
    
    # Google Drive
    GOOGLE_CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
    DRIVE_TOKEN_FILE = 'tokens/drive_token.json'
    
    # AI (OpenAI/Claude)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    AI_MODEL = os.getenv('AI_MODEL', 'gpt-3.5-turbo')
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    PORT = int(os.getenv('PORT', 5000))
