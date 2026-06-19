"""
bot.py — Entry point.

Registers all handlers and starts polling.
"""

import logging
from telegram.ext import ApplicationBuilder, CommandHandler

from config import BOT_TOKEN
from database import init_db
from start import start
from tracking import cmd_sleep, cmd_wake
from stats import cmd_stats, cmd_history
from settings import cmd_goal

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def post_init(app) -> None:
    """Called once after the app is built — init DB here."""
    await init_db()
    logger.info("Database initialized ✅")


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set. Check your .env file.")

    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    # Register commands
    app.add_handler(CommandHandler("start",   start))
    app.add_handler(CommandHandler("sleep",   cmd_sleep))
    app.add_handler(CommandHandler("wake",    cmd_wake))
    app.add_handler(CommandHandler("stats",   cmd_stats))
    app.add_handler(CommandHandler("history", cmd_history))
    app.add_handler(CommandHandler("goal",    cmd_goal))

    logger.info("Bot is running 🚀")
    app.run_polling()


if __name__ == "__main__":
    main()
