# 😴 Sleep Tracker Telegram Bot

Track your sleep schedule directly in Telegram.

## Features
- Log wake-up time
- Log sleep time
- Auto-calculate sleep duration
- Weekly progress chart (ASCII + stats)
- Daily reminders (optional)

## Commands
| Command | Description |
|---|---|
| `/wake [HH:MM]` | Log wake-up time (defaults to now) |
| `/sleep [HH:MM]` | Log sleep time (defaults to now) |
| `/stats` | Show this week's sleep stats |
| `/history [days]` | Show last N days log (default 7) |
| `/goal [hours]` | Set your daily sleep goal |
| `/start` | Welcome + instructions |

## Project Structure
```
sleep-bot/
├── bot.py              # Entry point, bot init
├── config.py           # Settings (token, DB path, defaults)
├── requirements.txt
├── models/
│   └── database.py     # SQLite schema + migrations
├── services/
│   ├── sleep_service.py    # Core business logic
│   └── stats_service.py    # Analytics & chart generation
├── handlers/
│   ├── start.py        # /start command
│   ├── tracking.py     # /wake, /sleep commands
│   ├── stats.py        # /stats, /history commands
│   └── settings.py     # /goal command
└── utils/
    └── time_parser.py  # Parse user time input (HH:MM, "now", etc.)
```

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env
# Set BOT_TOKEN in .env
python bot.py
```

