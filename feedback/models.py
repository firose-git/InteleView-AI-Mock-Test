from django.db import models
from testsystem.models import TestSession

class Feedback(models.Model):
    test_session = models.OneToOneField(TestSession, on_delete=models.CASCADE ,related_name='feedback')
    improvement_suggestions = models.TextField()
    resource_links = models.JSONField()  # e.g., {"GFG": "https://...", "PrepInsta": "https://..."}
    rating = models.IntegerField(default=0)
    user_comments = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback for Session {self.test_session.id}"
