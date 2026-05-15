from django.db import models


class Profile(models.Model):
    full_name = models.CharField(max_length=120)
    title = models.CharField(max_length=160, help_text="e.g. Python Developer | Backend Engineer")
    summary = models.TextField()
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=32, blank=True)
    telegram = models.CharField(max_length=64, blank=True)
    github = models.CharField(max_length=64, blank=True, help_text="GitHub username")
    linkedin = models.URLField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    cv_file = models.FileField(upload_to="cv/", blank=True, null=True)
    is_available = models.BooleanField(default=True, help_text="Open to work")

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def __str__(self):
        return self.full_name


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ("backend", "Back-End"),
        ("frontend", "Front-End"),
        ("database", "Databases"),
        ("tools", "Tools"),
        ("language", "Languages"),
    ]
    name = models.CharField(max_length=64)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="backend")
    level = models.PositiveSmallIntegerField(default=70, help_text="0-100")
    icon = models.CharField(max_length=64, blank=True, help_text="Lucide icon name, optional")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["category", "order", "-level"]

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Project(models.Model):
    title = models.CharField(max_length=140)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=240)
    description = models.TextField()
    tech_stack = models.CharField(max_length=240, help_text="Comma-separated")
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    image2 = models.ImageField(upload_to="projects/", blank=True, null=True)
    image3 = models.ImageField(upload_to="projects/", blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_confidential = models.BooleanField(default=False, help_text="Hides source code / sensitive info")
    users_count = models.PositiveIntegerField(default=0, help_text="Live users / customers (optional)")
    users_count_label = models.CharField(max_length=80, blank=True, help_text="e.g. '+3 today'")
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["-is_featured", "order", "-created_at"]

    def __str__(self):
        return self.title

    @property
    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]


class Experience(models.Model):
    role = models.CharField(max_length=140)
    company = models.CharField(max_length=140)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField()
    tech = models.CharField(max_length=240, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "-start_date"]

    def __str__(self):
        return f"{self.role} @ {self.company}"


class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    start_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "-start_year"]

    def __str__(self):
        return f"{self.degree} — {self.institution}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.subject or 'no subject'}"
