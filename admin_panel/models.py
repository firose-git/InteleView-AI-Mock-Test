from django.db import models
from users.models import UserProfile
from testsystem.models import QuestionBank

class AdminActionLog(models.Model):
    admin = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    action_type = models.CharField(max_length=100)  # e.g., "Approved Question"
    target_question = models.ForeignKey(QuestionBank, null=True, blank=True, on_delete=models.SET_NULL)
    action_timestamp = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.action_type} by {self.admin.username if self.admin else 'N/A'}"
