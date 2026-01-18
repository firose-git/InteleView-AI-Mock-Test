from django.contrib import admin
from .models import QuestionBank, TestSession, TabSwitchLog, CameraLog

@admin.register(QuestionBank)
class QuestionBankAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_type', 'company', 'difficulty', 'created_by', 'updated_at')
    search_fields = ('question_text', 'company', 'created_by__username')
    list_filter = ('question_type', 'difficulty')

@admin.register(TestSession)
class TestSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'round_type', 'started_at', 'completed_at', 'score')
    list_filter = ('round_type', 'started_at', 'completed_at')
    search_fields = ('user__username',)

@admin.register(TabSwitchLog)
class TabSwitchLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'test_session', 'timestamp', 'reason')
    search_fields = ('user__username', 'reason')

@admin.register(CameraLog)
class CameraLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'test_session', 'snapshot_time', 'image_url')
    search_fields = ('user__username',)
