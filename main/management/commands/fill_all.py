"""Auto-fill the portfolio with all data: project images, profile email, CV file.

Reads assets from ``seed_assets/`` (committed to repo) so it works on Render
after a fresh clone, not just on the developer's machine.
"""
from pathlib import Path
from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings
from main.models import Profile, Project

ASSETS = Path(settings.BASE_DIR) / "seed_assets"
PROJECTS_DIR = ASSETS / "projects"
CV_DIR = ASSETS / "cv"


def attach(model_instance, field_name, file_path):
    if not file_path.exists():
        print(f"  ! missing {file_path}")
        return False
    with open(file_path, "rb") as f:
        getattr(model_instance, field_name).save(file_path.name, File(f), save=False)
    return True


class Command(BaseCommand):
    help = "Fill profile + project images + CV from seed_assets/"

    def handle(self, *args, **opts):
        # 1) Profile email + CV
        p = Profile.objects.first()
        if not p:
            self.stdout.write(self.style.ERROR("No Profile in DB. Run `seed` first."))
            return
        p.email = "ukzabila@gmail.com"
        cv_source = CV_DIR / "CV_Aleksandr_Zabila.pdf"
        if attach(p, "cv_file", cv_source):
            print(f"  cv attached: {cv_source.name}")
        p.save()
        print(f"Profile updated: {p.full_name} <{p.email}>")

        # 2) Map screenshots to projects (slug -> (image, image2, image3))
        mapping = {
            "auto-pidkliuch": ("auto-pidkliuch.png", None, None),
            "weather-bot": ("weather-bot.png", None, None),
            "gerat-blackout-bot": ("blackout-schedule.png", "blackout-users.png", None),
            "transcriber-bot": (None, None, None),
            "finance-bot": ("finance-bot.png", None, None),
            "web-coursework": (None, None, None),
        }
        for slug, (img1, img2, img3) in mapping.items():
            proj = Project.objects.filter(slug=slug).first()
            if not proj:
                continue
            if img1: attach(proj, "image",  PROJECTS_DIR / img1)
            if img2: attach(proj, "image2", PROJECTS_DIR / img2)
            if img3: attach(proj, "image3", PROJECTS_DIR / img3)
            proj.save()
            print(f"  attached to {slug}: {img1 or '-'} / {img2 or '-'} / {img3 or '-'}")

        # 3) Add the real СТО Герат project
        gerat_crm, created = Project.objects.update_or_create(
            slug="sto-gerat-crm",
            defaults=dict(
                title='STO "Gerat" — Auto Service CRM & Shop',
                short_description=(
                    "Full-stack web CRM for an auto repair service: catalog, sales, "
                    "analytics, and inventory in one interface."
                ),
                description=(
                    "A production-grade web application built for STO «Gerat» — a real "
                    "auto service / parts shop. Replaces paper logs and Excel with a "
                    "single dashboard.\n\n"
                    "Modules:\n"
                    "- CRM with master service catalog (200+ jobs: brake pads, oil, "
                    "  filters, diagnostics, etc.) and real-time invoice builder\n"
                    "- Shop module with barcode scanning, stock counters, and receipt printing\n"
                    "- Analytics tab with revenue/orders charts, top services, top clients\n"
                    "- Role-based access (Admin / Cashier)\n"
                    "- Custom UI in dark theme with responsive layout"
                ),
                tech_stack="JavaScript, HTML, CSS, Chart.js, REST API",
                github_url="https://github.com/OleksanderZabila/gerat",
                is_featured=True,
                order=5,
            ),
        )
        attach(gerat_crm, "image",  PROJECTS_DIR / "gerat-shop.png")
        attach(gerat_crm, "image2", PROJECTS_DIR / "gerat-crm.png")
        attach(gerat_crm, "image3", PROJECTS_DIR / "gerat-analytics.png")
        gerat_crm.save()
        print(f"  {'created' if created else 'updated'}: {gerat_crm.title}")

        # 4) Remove vague placeholder
        deleted, _ = Project.objects.filter(slug="web-coursework").delete()
        if deleted:
            print("  removed: Web Coursework (replaced)")

        self.stdout.write(self.style.SUCCESS("Done."))
