"""GitHub API integration with caching."""
import logging
import requests
from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger(__name__)

GITHUB_API = "https://api.github.com"
CACHE_TTL = 60 * 60  # 1 hour


def _headers():
    h = {"Accept": "application/vnd.github+json", "User-Agent": "portfolio-site"}
    if settings.GITHUB_TOKEN:
        h["Authorization"] = f"Bearer {settings.GITHUB_TOKEN}"
    return h


def _get(url, params=None):
    try:
        r = requests.get(url, headers=_headers(), params=params, timeout=8)
        if r.status_code == 200:
            return r.json()
        logger.warning("GitHub API %s -> %s", url, r.status_code)
    except requests.RequestException as e:
        logger.warning("GitHub API request failed: %s", e)
    return None


def get_user(username=None):
    username = username or settings.GITHUB_USERNAME
    key = f"gh:user:{username}"
    cached = cache.get(key)
    if cached is not None:
        return cached
    data = _get(f"{GITHUB_API}/users/{username}") or {}
    cache.set(key, data, CACHE_TTL)
    return data


def get_repos(username=None, limit=12):
    username = username or settings.GITHUB_USERNAME
    key = f"gh:repos:{username}"
    cached = cache.get(key)
    if cached is None:
        data = _get(
            f"{GITHUB_API}/users/{username}/repos",
            params={"per_page": 100, "sort": "updated", "type": "owner"},
        ) or []
        cache.set(key, data, CACHE_TTL)
    else:
        data = cached

    cleaned = []
    for r in data:
        if r.get("fork"):
            continue
        cleaned.append({
            "name": r.get("name"),
            "description": r.get("description") or "",
            "language": r.get("language") or "Other",
            "stars": r.get("stargazers_count", 0),
            "forks": r.get("forks_count", 0),
            "url": r.get("html_url"),
            "homepage": r.get("homepage") or "",
            "size_kb": r.get("size", 0),
            "updated_at": r.get("updated_at", ""),
            "topics": r.get("topics", []),
        })
    cleaned.sort(key=lambda x: (-x["stars"], -x["size_kb"]))
    return cleaned[:limit]


def get_language_stats(username=None):
    repos = get_repos(username, limit=100)
    counter = {}
    for r in repos:
        lang = r["language"]
        counter[lang] = counter.get(lang, 0) + 1
    total = sum(counter.values()) or 1
    stats = [
        {"name": k, "count": v, "percent": round(v * 100 / total, 1)}
        for k, v in sorted(counter.items(), key=lambda x: -x[1])
    ]
    return stats[:8]


def notify_telegram(name, email, subject, message):
    """Send a contact-form message to a Telegram chat."""
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    if not token or not chat_id:
        logger.info("Telegram not configured; skipping notification.")
        return False
    text = (
        "📬 <b>New message from portfolio</b>\n\n"
        f"<b>From:</b> {name}\n"
        f"<b>Email:</b> <code>{email}</code>\n"
        f"<b>Subject:</b> {subject or '—'}\n\n"
        f"<b>Message:</b>\n{message}"
    )
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True},
            timeout=8,
        )
        if r.status_code == 200:
            return True
        logger.warning("Telegram sendMessage failed: %s %s", r.status_code, r.text[:200])
    except requests.RequestException as e:
        logger.warning("Telegram request error: %s", e)
    return False


def get_summary(username=None):
    repos_full = get_repos(username, limit=100)
    user = get_user(username)
    return {
        "user": user,
        "total_repos": len(repos_full),
        "total_stars": sum(r["stars"] for r in repos_full),
        "languages": get_language_stats(username),
    }
