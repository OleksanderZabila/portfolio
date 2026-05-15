from django.contrib import admin
from .models import Profile, Skill, Project, Experience, Education, ContactMessage


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "title", "email", "is_available")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "level", "order")
    list_editable = ("level", "order")
    list_filter = ("category",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "is_featured", "is_confidential", "users_count", "order", "created_at")
    list_editable = ("is_featured", "is_confidential", "order")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "tech_stack")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "start_date", "end_date")


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("degree", "institution", "start_year", "end_year")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_filter = ("is_read",)
    readonly_fields = ("name", "email", "subject", "message", "created_at")
