from django.db import models
from django.contrib.auth.models import AbstractUser


class Cook(AbstractUser):
    year_of_experience = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ("username",)
        verbose_name = "Cook"
        verbose_name_plural = "Cooks"

    def __str__(self):
        return self.username
