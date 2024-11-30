from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.forms import (
    CookRegisterForm,
    CookUpdateForm,
    CookSearchForm,
)
from accounts.models import Cook


class FormsTest(TestCase):
    def test_cook_search_form(self):
        form_data = {
            "username": "test_username",
        }
        form = CookSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_cook_create_form(self):
        form_data = {
            "username": "test_username",
            "email": "dDyYU@example.com",
            "password1": "Test_password123",
            "password2": "Test_password123",
            "year_of_experience": 45,
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        }
        form = CookRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
    
    def test_cook_update_form(self):
        form_data = {
            "username": "test_username",
            "email": "dDyYU@example.com",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "year_of_experience": 45,
        }
        form = CookUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
