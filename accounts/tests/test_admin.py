from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="username", password="password"
        )
        self.client.force_login(self.admin_user)
        self.cook = get_user_model().objects.create_user(
            username="cook",
            password="password",
            first_name="first_name",
            last_name="last_name",
            year_of_experience=10,
        )

    def test_cook_year_of_experience_listed(self):
        """
        Test that cook year of experience is displayed on cook list page
        """
        url = reverse("admin:accounts_cook_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.cook.year_of_experience)

    def test_cook_detail_year_of_experience_listed(self):
        """
        Test that cook year of experience is displayed on cook detail page
        """
        url = reverse("admin:accounts_cook_change", args=[self.cook.id])
        res = self.client.get(url)
        self.assertContains(res, self.cook.year_of_experience)

    def test_cook_add_year_of_experience_listed(self):
        """
        Test that cook year of experience is displayed on cook add page
        """
        url = reverse("admin:accounts_cook_add")
        res = self.client.get(url)
        self.assertContains(res, "Year of experience")
