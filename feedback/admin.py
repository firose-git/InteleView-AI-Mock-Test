from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'test_session', 'rating', 'updated_at')
    search_fields = ('test_session__user__username', 'user_comments')
    list_filter = ('rating', 'updated_at')
