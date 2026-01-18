from django.db import models
from django.utils import timezone
from users.models import UserProfile

QUESTION_TYPE = (
    ('aptitude', 'Aptitude'),
    ('technical', 'Technical'),
    ('gd', 'Group Discussion'),
    ('hr', 'HR'),
)

DIFFICULTY_LEVEL = (
    ('basic', 'Basic'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
)

class QuestionBank(models.Model):
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE)
    company = models.CharField(max_length=100, blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVEL)
    question_text = models.TextField()
    options = models.JSONField(null=True, blank=True)
    answer = models.TextField()
    created_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name="created_questions")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.question_type} - {self.company}"

class TestSession(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    round_type = models.CharField(max_length=20, choices=QUESTION_TYPE)
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(default=0.0)
    question_ids = models.JSONField()
    answers = models.JSONField()
    feedback_notes = models.TextField(blank=True, null=True)

    video_url = models.URLField(blank=True, null=True)
    ai_summary = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        # Add a runtime check to avoid error
        if self.user_id and self.user.username:
            return f"{self.user.username} - {self.round_type} Round"
        return f"Session {self.pk} - {self.round_type}"

class TabSwitchLog(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    test_session = models.ForeignKey(TestSession, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    screenshot_url = models.URLField(null=True, blank=True)
    reason = models.TextField(default="Tab Switch Detected")

    def __str__(self) -> str:
        return f"Tab Switch - {self.user.username if self.user_id else 'Unknown'}"

class CameraLog(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    test_session = models.ForeignKey(TestSession, on_delete=models.CASCADE)
    snapshot_time = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField()

    def __str__(self) -> str:
        return f"CameraLog - {self.user.username if self.user_id else 'Unknown'} @ {self.snapshot_time}"
