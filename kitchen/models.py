from django.conf import settings
from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    dish_type = models.ForeignKey(DishType, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cooks = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="cooks_dishes"
    )
    ingredients = models.ManyToManyField(Ingredient, related_name="ingredients_dishes")

    class Meta:
        verbose_name_plural = "Dishes"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "dish_type"], name="unique_dish_name_dish_type"
            )
        ]
        ordering = ["name"]

    def __str__(self):
        return self.name
