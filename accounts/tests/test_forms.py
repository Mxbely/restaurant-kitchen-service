from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory

from accounts.forms import (
    CookRegisterForm,
    CookUpdateForm,
    CookSearchForm,
    ChangePasswordForm,
    LoginForm,
)
from accounts.models import Cook


class FormsTest(TestCase):
    def test_cook_search_form(self):
        """Test that the cook search form is valid."""
        form_data = {
            "username": "test_username",
        }
        form = CookSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_cook_create_form(self):
        """Test that the cook create form is valid."""
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
        """Test that the cook update form is valid."""
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

    def test_change_password_form(self):
        """Test that the change password form is valid."""
        user = get_user_model().objects.create_user(
            username="user.user", password="Password12345"
        )
        form_data = {
            "old_password": "Password12345",
            "new_password1": "Sa12De34",
            "new_password2": "Sa12De34",
        }
        form = ChangePasswordForm(user=user, data=form_data)
        self.assertTrue(form.is_valid())
        cleaned_data = form.cleaned_data
        self.assertEqual(cleaned_data["new_password1"], "Sa12De34")
        self.assertEqual(cleaned_data["new_password2"], "Sa12De34")

    def test_cook_create_form_invalid_experience(self):
        """Test that the cook create form is invalid if the year of experience is negative."""
        form_data = {
            "username": "test_username",
            "email": "test@example.com",
            "password1": "Test_password123",
            "password2": "Test_password123",
            "year_of_experience": -1,
        }
        form = CookRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("year_of_experience", form.errors)

    def test_cook_create_form_duplicate_email(self):
        """Test that the cook create form is invalid if the email is already taken."""
        Cook.objects.create_user(
            username="existing_user",
            email="test@example.com",
            password="password123"
        )
        
        form_data = {
            "username": "new_user",
            "email": "test@example.com",
            "password1": "Test_password123",
            "password2": "Test_password123",
        }
        form = CookRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_login_form_valid(self):
        """Test that the login form is valid."""
        user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123"
        )
        
        form_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        request = RequestFactory().get('/')
        form = LoginForm(data=form_data, request=request)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid_credentials(self):
        """Test that the login form is invalid if the credentials are incorrect."""
        form_data = {
            "username": "nonexistent",
            "password": "wrongpass"
        }
        request = RequestFactory().get('/')
        form = LoginForm(data=form_data, request=request)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
