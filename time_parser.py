from datetime import datetime, timezone, timedelta
from typing import Optional

# UTC+5 для Алматы
ALMATY_TZ = timezone(timedelta(hours=5))

def parse_time(raw: Optional[str]) -> datetime:
    now = datetime.now(ALMATY_TZ)  # <- было timezone.utc

    if not raw or raw.strip().lower() in ("now", "сейчас", ""):
        return now

    raw = raw.strip()

    try:
        t = datetime.strptime(raw, "%H:%M")
        return now.replace(hour=t.hour, minute=t.minute, second=0, microsecond=0)
    except ValueError:
        pass

    try:
        t = datetime.strptime(raw, "%H:%M %d.%m")
        return now.replace(
            month=t.month, day=t.day,
            hour=t.hour, minute=t.minute,
            second=0, microsecond=0
        )
    except ValueError:
        pass

    raise ValueError(
        "Не понял формат времени 🤔\n"
        "Используй: `HH:MM` (например `07:30`) или просто напиши /wake без времени."
    )


def format_duration(hours: float) -> str:
    h = int(hours)
    m = int((hours - h) * 60)
    return f"{h} ч {m} мин"


def sleep_quality_emoji(hours: float, goal: float) -> str:
    ratio = hours / goal
    if ratio >= 0.95:
        return "✅"
    elif ratio >= 0.75:
        return "🟡"
    else:
        return "🔴"