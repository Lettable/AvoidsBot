from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv("API_ID"))
API_HASH = str(getenv("API_HASH", ""))
BOT_TOKEN = str(getenv("BOT_TOKEN", ""))
MONGO_DB_URI = str(getenv("MONGO_DB_URI", None))
IMAGE_URL = str(getenv("IMAGE_URL", ""))
AWAIT_ROOM_ID = int(getenv("AWAIT_ROOM_ID", None))
CHANNEL_ID = int(getenv("CHANNEL_ID", None))

def check():
    req = [API_ID, API_HASH, BOT_TOKEN, MONGO_DB_URI, IMAGE_URL, AWAIT_ROOM_ID, CHANNEL_ID]
    if None in req or "" in req:
        raise ValueError("One or more required environment variables are missing or empty. Please check your .env file.")

check()
