from django.contrib import admin
from .models import AdminActionLog

@admin.register(AdminActionLog)
class AdminActionLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'admin', 'action_type', 'target_question', 'action_timestamp')
    search_fields = ('admin__username', 'action_type', 'remarks')
    list_filter = ('action_type', 'action_timestamp')
