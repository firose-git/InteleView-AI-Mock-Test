# aptitude/admin.py
from django.contrib import admin
from .models import AptitudeQuestion, AptitudeAttempt

admin.site.register(AptitudeQuestion)
admin.site.register(AptitudeAttempt)
