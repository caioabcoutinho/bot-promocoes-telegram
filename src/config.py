import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
CHANNELS = [c.strip() for c in os.getenv("CHANNELS", "").split(",") if c.strip()]
USER_CHAT_ID = int(os.getenv("USER_CHAT_ID", 0))
DB_PATH = os.path.join("data", "monitor.db")
