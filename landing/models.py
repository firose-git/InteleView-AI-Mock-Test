from djongo import models
from datetime import datetime

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    submitted_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.name} - {self.email}"
