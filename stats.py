"""
Handlers for /stats and /history commands.
"""

from telegram import Update
from telegram.ext import ContextTypes
from sleep_service import SleepService
from stats_service import StatsService
from time_parser import format_duration
from config import DEFAULT_HISTORY_DAYS, MAX_HISTORY_DAYS

_sleep_svc = SleepService()
_stats_svc = StatsService()


async def cmd_stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /stats
    Show a weekly sleep progress chart + summary.
    """
    user = update.effective_user
    goal = await _sleep_svc.get_sleep_goal(user.id)
    sessions = await _sleep_svc.get_sessions(user.id, days=7)
    msg = _stats_svc.render_stats_message(sessions, goal, days=7)
    await update.message.reply_text(msg, parse_mode="Markdown")


async def cmd_history(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /history [N]
    Show the last N days of sleep logs (default 7, max 30).
    """
    user = update.effective_user

    days = DEFAULT_HISTORY_DAYS
    if ctx.args:
        try:
            days = min(int(ctx.args[0]), MAX_HISTORY_DAYS)
        except ValueError:
            await update.message.reply_text("Укажи количество дней числом, например: /history 14")
            return

    goal = await _sleep_svc.get_sleep_goal(user.id)
    sessions = await _sleep_svc.get_sessions(user.id, days=days)

    if not sessions:
        await update.message.reply_text(
            "📭 Нет записей за этот период.\n"
            "Начни с /sleep когда ложишься спать."
        )
        return

    lines = [f"📋 *История сна за {days} дней:*\n"]
    for s in reversed(sessions):  # newest first
        date_str = s["wake_time"].strftime("%d.%m")
        sleep_str = s["sleep_time"].strftime("%H:%M")
        wake_str = s["wake_time"].strftime("%H:%M")
        dur = format_duration(s["duration_hours"])
        from utils.time_parser import sleep_quality_emoji
        emoji = sleep_quality_emoji(s["duration_hours"], goal)
        lines.append(f"`{date_str}` {sleep_str}→{wake_str}  *{dur}* {emoji}")

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
