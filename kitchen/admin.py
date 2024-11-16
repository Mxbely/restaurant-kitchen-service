from django.contrib import admin
from .models import Ingredient, DishType, Dish, Cook
from django.contrib.auth.admin import UserAdmin


@admin.register(Ingredient)
class IngrediensAdmin(admin.ModelAdmin):
    pass


@admin.register(DishType)
class DishTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    pass


@admin.register(Cook)
class CookAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("year_of_experience",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info"), {"fields": ("year_of_experience",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (("Additional info"), {"fields": ("first_name", "last_name", "year_of_experience")}),
    )
