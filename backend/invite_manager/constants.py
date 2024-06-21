import os

from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 12302))

SERVICE_URI = f'http://{HOST}:{PORT}'

DB_NAME = os.getenv("DB_NAME", "detention_admin")
