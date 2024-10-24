from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.user_models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'image', 'get_additional_permissions')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extra Fields', {'fields': ('image', 'hourly_rate', 'additional_permissions')}),
    )
    list_filter = BaseUserAdmin.list_filter + ('image',)

admin.site.register(User, UserAdmin)


