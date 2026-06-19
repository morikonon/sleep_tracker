"""
Handler for /goal command — lets user update their sleep target.
"""

from telegram import Update
from telegram.ext import ContextTypes
from sleep_service import SleepService
from config import MIN_SLEEP_HOURS, MAX_SLEEP_HOURS

_svc = SleepService()


async def cmd_goal(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /goal [hours]
    Set or display the daily sleep goal.
    """
    user = update.effective_user

    if not ctx.args:
        current = await _svc.get_sleep_goal(user.id)
        await update.message.reply_text(
            f"🎯 Твоя текущая цель: *{current} ч*\n\n"
            "Чтобы изменить: `/goal 8.5`",
            parse_mode="Markdown",
        )
        return

    try:
        hours = float(ctx.args[0].replace(",", "."))
    except ValueError:
        await update.message.reply_text("Укажи число часов, например: `/goal 7.5`", parse_mode="Markdown")
        return

    if not (MIN_SLEEP_HOURS <= hours <= MAX_SLEEP_HOURS):
        await update.message.reply_text(
            f"Цель должна быть от {MIN_SLEEP_HOURS} до {MAX_SLEEP_HOURS} часов."
        )
        return

    await _svc.set_sleep_goal(user.id, hours)
    await update.message.reply_text(
        f"✅ Цель сна обновлена: *{hours} ч*",
        parse_mode="Markdown",
    )
