from django.contrib import admin
from .models import TechnicalQuestion, TechnicalAttempt

@admin.register(TechnicalQuestion)
class TechnicalQuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'question_type', 'question_text_truncated',
        'options_display', 'correct_answer', 'domain',
        'difficulty', 'explanation_truncated', 'created_at'
    )
    search_fields = ('question_text', 'domain', 'explanation')
    list_filter = ('question_type', 'domain', 'difficulty')
    ordering = ('-created_at',)
    list_per_page = 20

    def question_text_truncated(self, obj):
        return obj.question_text[:100] + '...' if len(obj.question_text) > 100 else obj.question_text
    question_text_truncated.short_description = 'Question'

    def options_display(self, obj):
        if obj.options and isinstance(obj.options, dict):
            return ', '.join([f"{k}: {v}" for k, v in obj.options.items()])
        return '-'
    options_display.short_description = 'Options'

    def explanation_truncated(self, obj):
        return obj.explanation[:60] + '...' if obj.explanation and len(obj.explanation) > 60 else obj.explanation
    explanation_truncated.short_description = 'Explanation'

@admin.register(TechnicalAttempt)
class TechnicalAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'is_correct', 'score', 'attempted_at')
    list_filter = ('is_correct', 'score', 'attempted_at')
    search_fields = ('user__username', 'question__question_text')
    ordering = ('-attempted_at',)
