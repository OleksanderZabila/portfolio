from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Profile, Skill, Project, Experience, Education, ContactMessage
from . import services


def home(request):
    profile = Profile.objects.first()
    skills_by_cat = {}
    for s in Skill.objects.all():
        skills_by_cat.setdefault(s.get_category_display(), []).append(s)

    gh_summary = services.get_summary()
    gh_repos = services.get_repos(limit=6)

    context = {
        "profile": profile,
        "skills_by_cat": skills_by_cat,
        "projects": Project.objects.all(),
        "experiences": Experience.objects.all(),
        "education": Education.objects.all(),
        "gh_summary": gh_summary,
        "gh_repos": gh_repos,
    }
    return render(request, "main/home.html", context)


def projects_all(request):
    gh_repos = services.get_repos(limit=50)
    return render(request, "main/projects.html", {
        "projects": Project.objects.all(),
        "gh_repos": gh_repos,
    })


@require_POST
def contact_submit(request):
    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    subject = request.POST.get("subject", "").strip()
    message = request.POST.get("message", "").strip()
    if name and email and message:
        ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
        services.notify_telegram(name, email, subject, message)
        messages.success(request, "Thanks! I'll get back to you soon.")
    else:
        messages.error(request, "Please fill in name, email, and message.")
    return redirect(request.META.get("HTTP_REFERER", "/") + "#contact")
