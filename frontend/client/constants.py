import os

from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 12999))

SERVICE_URI = f'http://{HOST}:{PORT}'

SESSION_ID_IDENTIFIER = 'seshhid-ddeeaadd'
