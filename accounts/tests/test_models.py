from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import Cook


class TestModels(TestCase):
    def test_cook_str(self):
        cook = Cook.objects.create(username="username")
        self.assertEqual(str(cook), "username")

    def test_cook_year_of_experience(self):
        cook = get_user_model().objects.create(
            username="username", 
            password="password", 
            year_of_experience=10,
        )
        self.assertEqual(cook.year_of_experience, 10)
