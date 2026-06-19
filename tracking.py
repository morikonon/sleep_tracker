"""
Handlers for /wake and /sleep commands.
"""

from telegram import Update
from telegram.ext import ContextTypes
from sleep_service import SleepService
from time_parser import parse_time, format_duration, sleep_quality_emoji

_svc = SleepService()


async def cmd_sleep(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /sleep [HH:MM]
    Log the time the user went to sleep.
    """
    user = update.effective_user
    await _svc.upsert_user(user.id, user.username)

    raw = " ".join(ctx.args) if ctx.args else None

    try:
        event_time = parse_time(raw)
    except ValueError as e:
        await update.message.reply_text(str(e), parse_mode="Markdown")
        return

    await _svc.log_event(user.id, "sleep", event_time)

    time_str = event_time.strftime("%H:%M")
    await update.message.reply_text(
        f"🌙 Зафиксировал: лёг спать в *{time_str}*\n\n"
        "Когда проснёшься — напиши /wake 😴",
        parse_mode="Markdown",
    )


async def cmd_wake(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /wake [HH:MM]
    Log the time the user woke up and show how long they slept.
    """
    user = update.effective_user
    await _svc.upsert_user(user.id, user.username)

    raw = " ".join(ctx.args) if ctx.args else None

    try:
        event_time = parse_time(raw)
    except ValueError as e:
        await update.message.reply_text(str(e), parse_mode="Markdown")
        return

    await _svc.log_event(user.id, "wake", event_time)

    # Try to compute duration from last sleep event
    last_sleep = await _svc.get_last_event(user.id, "sleep")
    goal = await _svc.get_sleep_goal(user.id)

    time_str = event_time.strftime("%H:%M")
    msg_lines = [f"☀️ Доброе утро! Проснулся в *{time_str}*"]

    if last_sleep and last_sleep < event_time:
        duration = (event_time - last_sleep).total_seconds() / 3600
        emoji = sleep_quality_emoji(duration, goal)
        msg_lines.append(
            f"\n⏱ Ты спал *{format_duration(duration)}* {emoji}"
        )
        msg_lines.append(f"🎯 Цель: {goal} ч")
    else:
        msg_lines.append("\n_(Не нашёл время засыпания — сначала используй /sleep)_")

    await update.message.reply_text("\n".join(msg_lines), parse_mode="Markdown")
