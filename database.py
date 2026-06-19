"""
Database layer — SQLite via aiosqlite.

Tables:
  users        — one row per Telegram user, stores preferences
  sleep_logs   — one row per sleep event (wake or sleep timestamp)
"""

import aiosqlite
from config import DB_PATH


CREATE_USERS = """
CREATE TABLE IF NOT EXISTS users (
    user_id     INTEGER PRIMARY KEY,
    username    TEXT,
    sleep_goal  REAL    NOT NULL DEFAULT 8.0,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);
"""

CREATE_SLEEP_LOGS = """
CREATE TABLE IF NOT EXISTS sleep_logs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users(user_id),
    event_type  TEXT    NOT NULL CHECK(event_type IN ('wake', 'sleep')),
    event_time  TEXT    NOT NULL,          -- ISO-8601 in UTC
    logged_at   TEXT    NOT NULL DEFAULT (datetime('now'))
);
"""

CREATE_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_logs_user_time ON sleep_logs(user_id, event_time DESC);",
]


async def init_db() -> None:
    """Run on startup — create tables if missing."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(CREATE_USERS)
        await db.execute(CREATE_SLEEP_LOGS)
        for idx in CREATE_INDEXES:
            await db.execute(idx)
        await db.commit()

async def get_connection():
    """Create a fresh connection every time."""
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    return db
