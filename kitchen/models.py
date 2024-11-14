from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import settings


class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class DishType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    dish_type = models.ForeignKey(DishType, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cooks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="dishes")
    ingredients = models.ManyToManyField(Ingredient, related_name="dishes")

    class Meta:
        verbose_name_plural = "Dishes"

    def __str__(self):
        return self.name


class Cook(AbstractUser):
    year_of_experience = models.PositiveIntegerField()

    class Meta:
        ordering = ("username",)

    def __str__(self):
        return self.username

