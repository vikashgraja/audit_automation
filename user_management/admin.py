from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Unit

class UserAdmin(BaseUserAdmin):
    list_display = ('employee_id', 'email', 'first_name', 'last_name', 'role', 'unit', 'is_staff')
    list_filter = ('role', 'unit', 'is_staff')
    fieldsets = (
        (None, {'fields': ('employee_id', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Role & Unit', {'fields': ('role', 'unit')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('employee_id', 'email', 'password', 'first_name', 'last_name', 'role', 'unit')}
        ),
    )
    search_fields = ('employee_id', 'email', 'first_name', 'last_name')
    ordering = ('employee_id',)

admin.site.register(User, UserAdmin)
admin.site.register(Unit)