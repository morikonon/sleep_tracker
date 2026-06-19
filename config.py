import os
from dotenv import load_dotenv
 
load_dotenv()
 
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
DB_PATH: str = os.getenv("DB_PATH", "/data/sleep_tracker.db")
 
DEFAULT_SLEEP_GOAL_HOURS: float = 8.0
MIN_SLEEP_HOURS: float = 1.0
MAX_SLEEP_HOURS: float = 24.0
 
# How many days back to show in /history by default
DEFAULT_HISTORY_DAYS: int = 7
MAX_HISTORY_DAYS: int = 30