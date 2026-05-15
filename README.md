# Portfolio — Aleksandr Zabila

> My personal portfolio site, built from scratch with Django. Dark-neon design, live GitHub integration, Telegram notifications for the contact form.

🌐 **Live demo:** [curfew-spree-kudos.ngrok-free.dev](https://curfew-spree-kudos.ngrok-free.dev) *(local tunnel — may go offline)*

📍 Cherkasy, Ukraine — open to work

---

## About

I'm a Computer Engineering student at **MAUP** (Master's, expected 2027), focused on Python backend development and PostgreSQL database design. I built this site to give recruiters a single place to see who I am, what I've shipped, and how I write code.

The site automatically pulls my latest GitHub repositories through the REST API, so the projects section is always up to date — no manual editing required.

---

## Features

- 🎨 **Dark-neon design** — animated gradient blobs, glass-morphism navbar, scroll-reveal animations, typewriter hero
- 🔌 **Live GitHub integration** — repos, stars, languages pulled from the GitHub API (cached for 1 hour to respect rate limits)
- 🤖 **Telegram notifications** — every contact-form submission is delivered to my Telegram in real time
- 🔒 **Confidential projects** — projects can be marked as private (e.g. my blackout-schedule bot serving 2 100+ users) and rendered with a lock badge instead of a code link
- 🖼️ **Project galleries** — up to 3 screenshots per project, auto-cycling on hover
- ⚙️ **Full Django admin** — every section (profile, skills, projects, experience, education, contact messages) is editable through the admin without touching code
- 📱 **Responsive** — works on phones, tablets, and desktops
- 🚀 **Production-ready** — WhiteNoise for static files, file-based cache, environment-based config

---

## Tech stack

| Layer | Tech |
|-------|------|
| Backend | Python 3.13, Django 6 |
| Database | SQLite (dev), PostgreSQL-ready (prod) |
| Frontend | Tailwind CSS, vanilla JavaScript |
| Integrations | GitHub REST API, Telegram Bot API |
| Static files | WhiteNoise + compressed manifest storage |
| Config | python-decouple (`.env`) |
| Deployment-ready | Render / Railway / VPS |

---

## Project structure

```
portfolio/
├── main/                       # Main app
│   ├── models.py               # Profile, Skill, Project, Experience, Education, ContactMessage
│   ├── views.py                # Page views + contact form handler
│   ├── services.py             # GitHub API client + Telegram notifier
│   ├── admin.py                # Customised Django admin
│   ├── context_processors.py   # site_profile available in every template
│   └── management/commands/
│       ├── seed.py             # Seed initial CV data
│       └── add_gerat.py        # Add the confidential Blackout Schedule Bot project
├── portfolio/                  # Project settings
│   ├── settings.py
│   └── urls.py
├── templates/
│   ├── base.html               # Layout with navbar, animated background, footer
│   └── main/
│       ├── home.html           # Single-page site (Hero / About / Skills / Projects / Experience / Contact)
│       └── projects.html       # Full repo list page
├── static/
│   ├── css/style.css
│   └── js/app.js               # Reveal, typewriter, skill bars, galleries
├── requirements.txt
├── .env.example
└── manage.py
```

---

## Getting started

```powershell
# 1. Clone
git clone https://github.com/OleksanderZabila/portfolio.git
cd portfolio

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1   # PowerShell
# source venv/bin/activate    # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
copy .env.example .env
# edit .env and fill in SECRET_KEY, GITHUB_USERNAME, etc.

# 5. Migrate database
python manage.py migrate

# 6. (Optional) Seed CV data
python manage.py seed
python manage.py add_gerat

# 7. Create admin user
python manage.py createsuperuser

# 8. Run
python manage.py runserver
```

Open <http://127.0.0.1:8000/> for the site and <http://127.0.0.1:8000/admin/> for the admin panel.

---

## Telegram notifications

Contact-form messages are delivered straight to my Telegram. Setup:

1. Create a bot through [@BotFather](https://t.me/BotFather), copy the token.
2. Send `/start` to your bot, then open `https://api.telegram.org/bot<TOKEN>/getUpdates` and grab `chat.id`.
3. Put both into `.env`:

   ```
   TELEGRAM_BOT_TOKEN=123456:ABC...
   TELEGRAM_CHAT_ID=987654321
   ```

If left empty, the form still works — messages are saved in the database and viewable in the admin.

---

## GitHub integration

The repo grid on the home page and the `/projects/` page are pulled directly from `https://api.github.com/users/<username>/repos`. Results are cached for 1 hour through Django's file-based cache, so we never hit the rate limit on production traffic.

For higher rate limits (60 → 5 000 req/h), add a `GITHUB_TOKEN` to `.env`. A token without scopes works — it just needs to exist.

---

## Featured projects

These are the projects highlighted on the site:

- **Blackout Schedule Bot** 🔒 — Telegram bot serving 2 100+ users with personalised Ukrainian power-outage schedules and live timeline charts. Source private.
- **Auto Pidkliuch** — desktop inventory management system (Python + PostgreSQL + Tkinter). Diploma project. Role-based access, analytics dashboard, full CRUD.
- **Weather Telegram Bot** — forecast bot with matplotlib-rendered temperature charts.
- **Transcriber Bot** — speech-to-text Telegram bot built as an interview challenge.

---

## Deployment notes

Tested locally on Windows 11 + Python 3.13. The project is ready to deploy on Render or Railway:

1. Set environment variables (`SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS=yourdomain.com`, `GITHUB_TOKEN`, Telegram vars).
2. Switch the database to PostgreSQL (Django settings support both via `DATABASES`).
3. `python manage.py collectstatic --noinput`.
4. Use Gunicorn or Uvicorn as the WSGI/ASGI server.

WhiteNoise already serves static files in production with gzip + manifest hashing.

---

## Contact

- 📬 [Telegram @ZabilaOleksandr](https://t.me/ZabilaOleksandr)
- 🐙 [GitHub @OleksanderZabila](https://github.com/OleksanderZabila)
- 📞 +380 50 838 4092
- 📍 Cherkasy, Ukraine

---

*Built with Django · Tailwind · ☕ · ❤️*
