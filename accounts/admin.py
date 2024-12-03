from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Cook


@admin.register(Cook)
class CookAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("year_of_experience",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info"), {"fields": ("year_of_experience",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            ("Additional info"),
            {"fields": ("first_name", "last_name", "year_of_experience")},
        ),
    )
