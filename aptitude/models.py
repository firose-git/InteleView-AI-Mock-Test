# ✅ step_apt_1: Set up Aptitude App Structure

# In terminal (if not yet done):
# python manage.py startapp aptitude

# aptitude/models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class AptitudeQuestion(models.Model):
    DOMAIN_CHOICES = [
        ('IT', 'IT'),
        ('Non-IT', 'Non-IT')
    ]
    SECTION_CHOICES = [
        ('Verbal', 'Verbal'),
        ('Reasoning', 'Reasoning'),
        ('Numerical', 'Numerical')
    ]

    domain = models.CharField(max_length=20, choices=DOMAIN_CHOICES)
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    company = models.CharField(max_length=100)
    question_text = models.TextField()
    options = models.JSONField()  # Example: ["A", "B", "C", "D"]
    answer = models.CharField(max_length=10)  # Example: "A"

    def __str__(self):
        return f"{self.company} - {self.section}"


class AptitudeAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(AptitudeQuestion, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=10)
    is_correct = models.BooleanField()
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.question.id}"

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ...
    user_type = models.CharField(max_length=50, choices=[
        ('student', 'Student'),
        ('professional', 'Professional'),
        ('trial', 'Trial'),
    ])



