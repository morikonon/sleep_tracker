from telegram import Update
from telegram.ext import ContextTypes
from sleep_service import SleepService

_svc = SleepService()


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await _svc.upsert_user(user.id, user.username)

    await update.message.reply_text(
        f"Привет, {user.first_name}! 😴\n\n"
        "Я помогу тебе следить за режимом сна.\n\n"
        "*Команды:*\n"
        "  /sleep `[HH:MM]` — записать время засыпания\n"
        "  /wake `[HH:MM]`  — записать время пробуждения\n"
        "  /stats           — статистика за неделю\n"
        "  /history `[дней]`— история записей\n"
        "  /goal `[часов]`  — установить цель сна\n\n"
        "Если не указать время — запишу текущее 🕐",
        parse_mode="Markdown",
    )
