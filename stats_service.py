"""
StatsService — compute analytics and render ASCII progress charts.
"""

from typing import Optional
from time_parser import format_duration, sleep_quality_emoji


class StatsService:

    def compute_summary(self, sessions: list[dict], goal: float) -> dict:
        """Aggregate sessions into a summary dict."""
        if not sessions:
            return {"count": 0}

        durations = [s["duration_hours"] for s in sessions]
        avg = sum(durations) / len(durations)
        best = max(durations)
        worst = min(durations)
        days_on_goal = sum(1 for d in durations if d >= goal * 0.95)

        return {
            "count": len(sessions),
            "avg_hours": round(avg, 2),
            "best_hours": round(best, 2),
            "worst_hours": round(worst, 2),
            "days_on_goal": days_on_goal,
            "goal": goal,
        }

    def render_weekly_chart(self, sessions: list[dict], goal: float) -> str:
        """
        Render a simple ASCII bar chart of the last sessions.

        Example output:
          Пн  ████████░░  7.5 ч ✅
          Вт  ██████████  8.2 ч ✅
          Ср  ██████░░░░  6.0 ч 🟡
          ...
        """
        if not sessions:
            return "📭 Нет данных за этот период."

        BAR_WIDTH = 10
        DAY_NAMES = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        lines = ["📊 *График сна:*\n"]

        for s in sessions[-7:]:  # show last 7 sessions max
            day_name = DAY_NAMES[s["wake_time"].weekday()]
            hours = s["duration_hours"]
            filled = min(int((hours / goal) * BAR_WIDTH), BAR_WIDTH)
            empty = BAR_WIDTH - filled
            bar = "█" * filled + "░" * empty
            emoji = sleep_quality_emoji(hours, goal)
            label = format_duration(hours)
            lines.append(f"`{day_name}  {bar}  {label}` {emoji}")

        return "\n".join(lines)

    def render_stats_message(
        self, sessions: list[dict], goal: float, days: int
    ) -> str:
        """Full stats message combining chart + summary."""
        chart = self.render_weekly_chart(sessions, goal)
        summary = self.compute_summary(sessions, goal)

        if summary["count"] == 0:
            return (
                "😴 Ещё нет записей о сне.\n\n"
                "Используй /sleep когда ложишься и /wake когда просыпаешься."
            )

        lines = [
            chart,
            "",
            f"📈 *Статистика за {days} дней:*",
            f"  Среднее:     `{format_duration(summary['avg_hours'])}`",
            f"  Лучшая ночь: `{format_duration(summary['best_hours'])}`",
            f"  Худшая ночь: `{format_duration(summary['worst_hours'])}`",
            f"  Цель ({summary['goal']} ч):  `{summary['days_on_goal']}/{summary['count']}` дней",
        ]

        # Motivational footer
        ratio = summary["avg_hours"] / goal
        if ratio >= 0.95:
            lines.append("\n🌟 Отличный режим! Так держать!")
        elif ratio >= 0.75:
            lines.append("\n💪 Почти у цели. Ложись чуть раньше!")
        else:
            lines.append("\n⚠️ Недосыпаешь. Попробуй установить напоминание.")

        return "\n".join(lines)
