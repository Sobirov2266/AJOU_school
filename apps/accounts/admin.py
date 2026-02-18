from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, TeacherProfile, StudentProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Role information", {"fields": ("role",)}),
        ("Profile", {"fields": ("profile_photo",)}),
        ("Security", {"fields": ("must_change_password",)}),
    )

    list_display = ("username", "email", "role", "must_change_password", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")


admin.site.register(TeacherProfile)
admin.site.register(StudentProfile)
