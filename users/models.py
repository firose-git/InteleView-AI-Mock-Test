from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
import uuid

USER_TYPE_CHOICES = (
    ('student', 'Student'),
    ('professional', 'Professional'),
    ('trial', 'Trial User'),
)

DEPARTMENT_CHOICES = [
    ("IT", "IT"),
    ("Non-IT", "Non-IT"),
]

class UserProfile(AbstractUser):
    # Core Fields
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    # Interview Metrics
    attempts_left = models.IntegerField(default=5)
    score = models.FloatField(default=0.0)
    rating = models.IntegerField(default=0)

    # Preferences & Settings
    camera_enabled = models.BooleanField(default=False)
    sound_enabled = models.BooleanField(default=False)
    tab_alert = models.BooleanField(default=False)
    email_notify = models.BooleanField(default=True)
    push_notify = models.BooleanField(default=False)

    # Career Preferences
    job_interest = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    salary_range = models.CharField(max_length=50, blank=True, null=True)

    # Email/OTP Verification
    email_verified = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    # Password Reset Support
    reset_token = models.CharField(max_length=64, null=True, blank=True)
    reset_requested_at = models.DateTimeField(null=True, blank=True)

    # Permissions (for admin panel compatibility)
    groups = models.ManyToManyField(
        Group,
        related_name='custom_userprofile_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_userprofile_permissions',
        blank=True
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def generate_otp(self):
        import random
        self.otp_code = f"{random.randint(1000, 9999)}"
        self.otp_created_at = timezone.now()
        self.save()

    def generate_reset_token(self):
        self.reset_token = uuid.uuid4().hex
        self.reset_requested_at = timezone.now()
        self.save()
