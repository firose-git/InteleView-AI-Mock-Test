from django.db import models

class GDResponse(models.Model):
    topic = models.CharField(max_length=255)
    transcript = models.TextField()
    fluency = models.IntegerField()
    vocabulary = models.IntegerField()
    clarity = models.IntegerField()
    confidence = models.IntegerField()
    summary = models.TextField()
    suggestions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
