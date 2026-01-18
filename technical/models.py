from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class TechnicalQuestion(models.Model):
    QUESTION_TYPES = [('mcq', 'MCQ'), ('code', 'Coding')]

    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    question_text = models.TextField()
    options = models.JSONField(blank=True, null=True)  # {"A": "...", "B": "..."}
    correct_answer = models.CharField(max_length=10, blank=True, null=True)  # For MCQ
    test_cases = models.JSONField(blank=True, null=True)  # For coding
    domain = models.CharField(max_length=100)  # Python, DBMS etc
    difficulty = models.CharField(max_length=20, default='Intermediate')
    explanation = models.TextField(blank=True, null=True)  # ✅ NEW FIELD
    created_at = models.DateTimeField(auto_now_add=True)

class TechnicalAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(TechnicalQuestion, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=10, null=True, blank=True)
    submitted_code = models.TextField(null=True, blank=True)
    is_correct = models.BooleanField(null=True)
    score = models.FloatField(default=0)
    attempted_at = models.DateTimeField(auto_now_add=True)
