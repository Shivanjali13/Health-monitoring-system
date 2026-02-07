from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email','username','age','gender','is_staff','created_at')
    list_filter = ('is_staff','is_active','gender')
    search_fields = ('email','username')
    ordering = ('-created_at',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Health Profile', {'fields': ('age','height','gender')}),
    )
# Register your models here.
