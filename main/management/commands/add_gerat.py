"""Add or update the gerat (blackout schedule bot) project."""
from datetime import date
from django.core.management.base import BaseCommand
from main.models import Project


class Command(BaseCommand):
    help = "Add/update gerat (blackout schedule Telegram bot)"

    def handle(self, *args, **opts):
        p, created = Project.objects.update_or_create(
            slug="gerat-blackout-bot",
            defaults=dict(
                title="Blackout Schedule Bot",
                short_description=(
                    "Telegram bot that delivers personalized power-outage schedules with "
                    "real-time charts. Used daily by 2000+ Ukrainians."
                ),
                description=(
                    "A production Telegram bot helping users navigate scheduled power "
                    "outages in Ukraine. Features:\n\n"
                    "- Per-group outage schedules (1.1, 1.2, ..., 6.2) with timeline charts\n"
                    "- Daily/hourly notifications based on user preferences\n"
                    "- Visual hour-by-hour timeline with current-time marker\n"
                    "- Admin analytics: new-user notifications, daily growth, total user count\n"
                    "- Scalable backend with persistent user storage\n\n"
                    "Source code is private; the bot is live and serving real users."
                ),
                tech_stack="Python, python-telegram-bot, matplotlib, SQLite, asyncio",
                github_url="",
                live_url="",
                is_featured=True,
                is_confidential=True,
                users_count=2142,
                users_count_label="+3 today",
                order=0,
                created_at=date(2026, 4, 21),
            ),
        )
        msg = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{msg}: {p.title}"))
