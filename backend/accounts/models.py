from django.contrib.auth.models import AbstractUser
from django.db import models
from pgvector.django import VectorField


class User(AbstractUser):

    email = models.EmailField(unique=True)
    google_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )
    profile_picture = models.URLField(
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class UserProfile(models.Model):

    class ExperienceLevel(models.TextChoices):
        NONE = "none", "None"
        INTERN = "intern", "Intern"
        JUNIOR = "junior", "Junior"
        MID_LEVEL = "mid_level", "Mid-level"
        SENIOR = "senior", "Senior"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
        )

    # Career Information

    primary_role = models.CharField(
        max_length=150,
        blank=True
    )

    target_role = models.CharField(
        max_length=150,
        blank=True
    )

    experience_level = models.CharField(
        max_length=20,
        choices=ExperienceLevel.choices,
        blank=True
    )

    # Education

    education = models.JSONField(
        default=list,
        blank=True
    )

    # Example:
    # [
    #     {
    #         "degree": "Bachelor of Computer Engineering",
    #         "institution": "XYZ University",
    #         "field": "Computer Engineering",
    #         "start_year": 2022,
    #         "end_year": 2026
    #     }
    # ]

    #skills

    skills = models.JSONField(
        default=list,
        blank=True
    )

    # Example:
    # [
    #     {"name": "Python", "level": "Advanced"},
    #     {"name": "Django", "level": "Intermediate"},
    #     {"name": "React", "level": "Intermediate"},
    #     {"name": "PostgreSQL", "level": "Intermediate"},
    #     {"name": "Machine Learning", "level": "Beginner"}
    # ]

    # Projects
    projects = models.JSONField(
        default=list,
        blank=True
    )

    # Example:
    # [
    #     {
    #         "title": "AI Interview System",
    #         "description": "...",
    #         "technologies": ["Django", "React", "PostgreSQL"],
    #         "role": "Backend Developer"
    #     }
    # ]

    # Professional Experience


    experience = models.JSONField(
        default=list,
        blank=True
    )

    # Example:
    # [
    #     {
    #         "company": "ABC",
    #         "position": "Software Intern",
    #         "description": "...",
    #         "start_date": "2025-06-01",
    #         "end_date": "2025-08-30"
    #     }
    # ]

    certifications = models.JSONField(
        default=list,
        blank=True
    )

    # AI / Vector Search

    profile_embedding = VectorField(
        dimensions=768,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.email}'s Profile"