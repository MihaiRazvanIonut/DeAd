import os

from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 12301))

SERVICE_URI = f'http://{HOST}:{PORT}'

MAX_IMAGE_SIZE = 8_000_000  # bytes

IMAGES_DIR_PATH = './images'
