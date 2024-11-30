from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


COOK_LIST_URL = reverse("accounts:cook-list")
COOK_DETAIL_URL = reverse("accounts:cook-detail", args=[1])


class PublicTests(TestCase):
    def test_cook_login_required(self):
        res = self.client.get(COOK_DETAIL_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "password123",
        )
        self.client.force_login(self.user)

    def test_retrieve_cook(self):
        get_user_model().objects.create_user(username="username", password="password")
        get_user_model().objects.create_user(username="username1", password="password1")
        res = self.client.get(COOK_LIST_URL)
        cooks = get_user_model().objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["cook_list"]), list(cooks))
        self.assertTemplateUsed(res, "accounts/cook_list.html")
