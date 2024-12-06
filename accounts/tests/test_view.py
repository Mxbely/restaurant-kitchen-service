from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.test import Client


COOK_LIST_URL = reverse("accounts:cook-list")
COOK_DETAIL_URL = reverse("accounts:cook-detail", args=[1])
LOGIN_URL = reverse("accounts:login")


class PublicTests(TestCase):
    def test_cook_login_required_cook_detail(self):
        """Test that accessing the cook detail view requires login."""
        res = self.client.get(COOK_DETAIL_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_cook_login_required_cook_list(self):
        """Test that the cook list view is accessible without login and that created cooks are present in the list."""
        res = self.client.get(COOK_LIST_URL)
        self.assertEqual(res.status_code, 200)
        cook1 = get_user_model().objects.create_user(
            username="user1", password="password1"
        )
        cook2 = get_user_model().objects.create_user(
            username="user2", password="password2"
        )
        cooks = get_user_model().objects.all()
        self.assertIn(cook1, list(cooks))


class PrivateTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "password123",
        )
        self.client.force_login(self.user)

    def test_retrieve_cook(self):
        """Test that a logged in user can retrieve a list of all cooks."""
        res = self.client.get(COOK_DETAIL_URL)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.user, res.context["user"])
        self.assertTemplateUsed(res, "accounts/cook_detail.html")


class RegisterViewTest(TestCase):
    def setUp(self):
        self.register_url = reverse(
            "accounts:register"
        )
        self.user_model = get_user_model()

    def test_register_view_get(self):
        """Test that the register page renders correctly."""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertContains(response, "form")

    def test_register_view_post_valid_data(self):
        """Test registering a new user with valid data."""
        valid_data = {
            "username": "testuser",
            "password1": "TestPassword123",
            "password2": "TestPassword123",
        }
        response = self.client.post(self.register_url, data=valid_data)
        self.assertEqual(self.user_model.objects.count(), 1)
        user = self.user_model.objects.get(username="testuser")
        self.assertTrue(user.check_password("TestPassword123"))
        self.assertIn("_auth_user_id", self.client.session)
        self.assertRedirects(response, reverse("kitchen:index"))

    def test_register_view_post_invalid_data(self):
        """Test posting invalid data."""
        invalid_data = {
            "username": "testuser",
            "password1": "password",
            "password2": "different_password",
        }
        response = self.client.post(self.register_url, data=invalid_data)
        self.assertEqual(self.user_model.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")

    def test_register_view_post_missing_data(self):
        """Test posting incomplete data."""
        missing_data = {
            "username": "",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(self.register_url, data=missing_data)
        self.assertEqual(self.user_model.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")


class StatusCodeTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="user1",
            password="password123"
        )
        self.other_user = get_user_model().objects.create_user(
            username="user2",
            password="password234"
        )

    def test_404_on_no_exist_cook(self):
        """Test that return 404 for no-exist cooks id."""
        self.client.force_login(self.user)
        no_exist_id = 0
        detail_url = reverse("accounts:cook-detail", args=[no_exist_id])
        update_url = reverse("accounts:cook-update", args=[no_exist_id])
        delete_url = reverse("accounts:cook-delete", args=[no_exist_id])
        self.assertEqual(self.client.get(detail_url).status_code, 404)
        self.assertEqual(self.client.get(update_url).status_code, 404)
        self.assertEqual(self.client.get(delete_url).status_code, 404)

    def test_redirect_after_login_required(self):
        """Test that protected views redirect to the login page."""
        protected_urls = [
            reverse("accounts:cook-detail", args=[self.user.id]),
            reverse("accounts:cook-update", args=[self.user.id]),
            reverse("accounts:cook-delete", args=[self.user.id]),
            reverse("accounts:change-password", args=[self.user.id]),
        ]

        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)

