"""
SleepService — all DB mutations related to sleep tracking.
"""

import aiosqlite
from datetime import datetime
from typing import Optional
from config import DB_PATH


class SleepService:

    # ------------------------------------------------------------------ users

    async def upsert_user(self, user_id: int, username: Optional[str]) -> None:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            await db.execute(
                """
                INSERT INTO users (user_id, username)
                VALUES (?, ?)
                ON CONFLICT(user_id) DO UPDATE SET username = excluded.username
                """,
                (user_id, username),
            )
            await db.commit()

    async def get_sleep_goal(self, user_id: int) -> float:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT sleep_goal FROM users WHERE user_id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return row["sleep_goal"] if row else 8.0

    async def set_sleep_goal(self, user_id: int, hours: float) -> None:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "UPDATE users SET sleep_goal = ? WHERE user_id = ?",
                (hours, user_id),
            )
            await db.commit()

    # ------------------------------------------------------------------ events

    async def log_event(
        self, user_id: int, event_type: str, event_time: datetime
    ) -> None:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "INSERT INTO sleep_logs (user_id, event_type, event_time) VALUES (?, ?, ?)",
                (user_id, event_type, event_time.isoformat()),
            )
            await db.commit()

    async def get_last_event(self, user_id: int, event_type: str) -> Optional[datetime]:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                """
                SELECT event_time FROM sleep_logs
                WHERE user_id = ? AND event_type = ?
                ORDER BY event_time DESC LIMIT 1
                """,
                (user_id, event_type),
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return datetime.fromisoformat(row["event_time"])
                return None

    # ------------------------------------------------------------------ sessions

    async def get_sessions(self, user_id: int, days: int = 7) -> list:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                """
                SELECT event_type, event_time FROM sleep_logs
                WHERE user_id = ?
                  AND event_time >= datetime('now', ?)
                ORDER BY event_time ASC
                """,
                (user_id, f"-{days} days"),
            ) as cursor:
                rows = await cursor.fetchall()

        events = [
            {"type": r["event_type"], "time": datetime.fromisoformat(r["event_time"])}
            for r in rows
        ]

        sessions = []
        pending_sleep: Optional[datetime] = None

        for ev in events:
            if ev["type"] == "sleep":
                pending_sleep = ev["time"]
            elif ev["type"] == "wake" and pending_sleep is not None:
                duration = (ev["time"] - pending_sleep).total_seconds() / 3600
                sessions.append(
                    {
                        "sleep_time": pending_sleep,
                        "wake_time": ev["time"],
                        "duration_hours": round(duration, 2),
                    }
                )
                pending_sleep = None

        return sessions