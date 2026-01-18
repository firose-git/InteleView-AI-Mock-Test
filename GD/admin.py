from django.contrib import admin
from .models import GDResponse

@admin.register(GDResponse)
class GDResponseAdmin(admin.ModelAdmin):
    list_display = ('topic', 'fluency', 'clarity', 'created_at')
    search_fields = ('topic', 'summary')
