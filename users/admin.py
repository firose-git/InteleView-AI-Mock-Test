from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

@admin.register(UserProfile)
class CustomUserAdmin(UserAdmin):
    model = UserProfile
    list_display = ('username', 'email', 'user_type', 'score', 'rating', 'attempts_left', 'is_active', 'is_staff')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('-updated_at',)

    fieldsets = (
        *(UserAdmin.fieldsets or ()),
        ('Custom Fields', {
            'fields': ('user_type', 'resume', 'attempts_left', 'score', 'rating')
        }),
    )
