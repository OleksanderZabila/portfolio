"""Seed initial data from CV."""
from datetime import date
from django.core.management.base import BaseCommand
from main.models import Profile, Skill, Project, Experience, Education


class Command(BaseCommand):
    help = "Seed portfolio with Aleksandr Zabila's CV data"

    def handle(self, *args, **opts):
        Profile.objects.all().delete()
        Skill.objects.all().delete()
        Project.objects.all().delete()
        Experience.objects.all().delete()
        Education.objects.all().delete()

        Profile.objects.create(
            full_name="Aleksandr Zabila",
            title="Junior Python Developer",
            summary=(
                "Python developer focused on backend systems and Telegram bots. Worked "
                "with Python, Django, python-telegram-bot, PostgreSQL, and SQLite — "
                "built a production Telegram bot currently serving 2,100+ daily users, "
                "a desktop CRM for a real auto-parts shop, and a web CRM/POS system "
                "for an auto service.\n\n"
                "Completing a Master's in Computer Engineering at MAUP. Looking for "
                "an opportunity to gain commercial experience in a strong engineering "
                "team and grow into a confident backend engineer."
            ),
            email="ukzabila@gmail.com",
            phone="+380508384092",
            telegram="ZabilaOleksandr",
            github="OleksanderZabila",
            linkedin="https://www.linkedin.com/in/oleksandr-zabila-274aab353/",
            location="Cherkasy, Ukraine",
            is_available=True,
        )

        # Skills are shown as plain chips (no progress bars / percentages).
        # The level field exists in the model for sorting only.
        skills = [
            ("Python", "backend", 1),
            ("Django", "backend", 2),
            ("python-telegram-bot", "backend", 3),
            ("C++", "backend", 4),
            ("Tkinter", "backend", 5),
            ("PostgreSQL", "backend", 6),
            ("SQLite", "backend", 7),
            ("SQL", "backend", 8),
            ("REST APIs", "backend", 9),
            ("HTML", "frontend", 1),
            ("CSS", "frontend", 2),
            ("Tailwind CSS", "frontend", 3),
            ("JavaScript", "frontend", 4),
            ("Git", "tools", 1),
            ("GitHub", "tools", 2),
            ("PyCharm", "tools", 3),
            ("VS Code", "tools", 4),
            ("pgAdmin", "tools", 5),
            ("matplotlib", "tools", 6),
            ("Terminal / PowerShell", "tools", 7),
            ("Ukrainian — Native", "language", 1),
            ("English — A2", "language", 2),
        ]
        for name, cat, o in skills:
            Skill.objects.create(name=name, category=cat, level=0, order=o)

        Project.objects.create(
            title="Inventory Management System — Auto Pidkliuch",
            slug="auto-pidkliuch",
            short_description="Desktop inventory system for an auto parts store with role-based access and analytics.",
            description=(
                "Diploma project: a full-featured inventory management system for an auto "
                "parts store. Implemented full CRUD for products, categories, suppliers, "
                "and customers; role-based access control (Admin / Cashier); analytics "
                "dashboard for sales tracking and reporting. PostgreSQL as the main DB, "
                "Tkinter for the GUI."
            ),
            tech_stack="Python, PostgreSQL, Tkinter, psycopg2",
            github_url="https://github.com/OleksanderZabila/DiplomWork",
            is_featured=True,
            order=1,
            created_at=date(2025, 3, 30),
        )
        Project.objects.create(
            title="Weather Forecast Telegram Bot",
            slug="weather-bot",
            short_description="Telegram bot that delivers weather forecasts with visual charts and diagrams.",
            description=(
                "Personal hobby project. Built a weather bot with command handling, "
                "user interaction, and chart-based visualizations of forecasts."
            ),
            tech_stack="Python, python-telegram-bot, matplotlib",
            github_url="https://github.com/OleksanderZabila/weather_telegram_bot-master",
            is_featured=True,
            order=2,
            created_at=date(2023, 12, 15),
        )
        Project.objects.create(
            title="Transcriber Bot",
            slug="transcriber-bot",
            short_description="Interview task — Telegram bot for audio transcription.",
            description="Telegram bot built as an interview challenge. Handles audio files, processes them and returns transcribed text.",
            tech_stack="Python, python-telegram-bot, speech-to-text",
            github_url="https://github.com/OleksanderZabila/transcriber-bot",
            is_featured=True,
            order=3,
            created_at=date(2025, 10, 8),
        )
        Project.objects.create(
            title="Personal Finance Telegram Bot",
            slug="finance-bot",
            short_description="Bot for logging and analyzing personal/home expenses with categories and summaries.",
            description=(
                "Personal pet project — a small Telegram bot I use myself to log daily "
                "expenses, categorise them, and print a quick summary. Stores data in "
                "SQLite locally; no commercial deployment."
            ),
            tech_stack="Python, python-telegram-bot, SQLite",
            github_url="",
            is_confidential=True,
            is_featured=False,
            order=4,
        )
        Project.objects.create(
            title="Static Business Card Sites & Browser Game",
            slug="web-coursework",
            short_description="Two static business-card websites and a simple browser game with responsive design.",
            description="Coursework projects — practiced HTML/CSS/JS, responsive layout, and cross-device compatibility.",
            tech_stack="HTML, CSS, JavaScript",
            github_url="https://github.com/OleksanderZabila/auto5",
            is_featured=False,
            order=5,
        )

        Experience.objects.create(
            role="Diploma Project Developer",
            company="Auto Pidkliuch (Auto Parts Store)",
            start_date=date(2025, 2, 1),
            end_date=date(2025, 5, 1),
            description=(
                "Designed and built an end-to-end inventory management system used "
                "internally by an auto parts store. Owned the project from database "
                "schema design through to GUI implementation and deployment."
            ),
            tech="Python · PostgreSQL · Tkinter",
            order=1,
        )
        Experience.objects.create(
            role="Hobby Developer — Telegram Bots",
            company="Personal Projects",
            start_date=date(2023, 12, 1),
            description=(
                "Building Telegram bots for personal use: weather forecasts with charts, "
                "home expense tracking, and other utilities. Focus on clean command "
                "handling and a smooth user experience."
            ),
            tech="Python · python-telegram-bot",
            order=2,
        )

        Education.objects.create(
            institution="Interregional Academy of Personnel Management (MAUP)",
            degree="Master's Degree in Computer Engineering",
            start_year=2021,
            end_year=2027,
            description=(
                "Studying online in the Computer Engineering specialty (121). "
                "Completed Bachelor's degree as part of the same academic program. "
                "Expected Master's graduation: 2027."
            ),
            location="Odesa, Ukraine",
            order=1,
        )
        Education.objects.create(
            institution="Online English Language Courses",
            degree="English — Level A2",
            start_year=2024,
            description="Improving communication skills to prepare for work in international teams.",
            order=2,
        )

        self.stdout.write(self.style.SUCCESS("OK - Seeded profile, skills, projects, experience, education"))
