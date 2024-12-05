from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from blog.models.costum_user import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'role')
    ordering = ('username',)
admin.site.register(CustomUser,CustomUserAdmin)