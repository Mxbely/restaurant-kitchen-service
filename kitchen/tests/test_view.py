from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import Dish, DishType, Ingredient

INDEX_URL = reverse("kitchen:index")

DISH_LIST_URL = reverse("kitchen:dish-list")
DISH_DETAIL_URL = reverse("kitchen:dish-detail", args=[1])
DISH_CREATE_URL = reverse("kitchen:dish-create")
DISH_UPDATE_URL = reverse("kitchen:dish-update", args=[1])
DISH_DELETE_URL = reverse("kitchen:dish-delete", args=[1])

DISH_TYPE_LIST_URL = reverse("kitchen:dish-type-list")
DISH_TYPE_CREATE_URL = reverse("kitchen:dish-type-create")
DISH_TYPE_UPDATE_URL = reverse("kitchen:dish-type-update", args=[1])
DISH_TYPE_DELETE_URL = reverse("kitchen:dish-type-delete", args=[1])

INGREDIENT_LIST_URL = reverse("kitchen:ingredient-list")
INGREDIENT_CREATE_URL = reverse("kitchen:ingredient-create")
INGREDIENT_UPDATE_URL = reverse("kitchen:ingredient-update", args=[1])
INGREDIENT_DELETE_URL = reverse("kitchen:ingredient-delete", args=[1])

ABOUT_URL = reverse("kitchen:about")
CONTACT_URL = reverse("kitchen:contact")


class PublicTests(TestCase):

    def test_index_required(self):
        """Test that the index page is accessible without login."""
        res = self.client.get(INDEX_URL)
        self.assertEqual(res.status_code, 200)

    def test_dish_detail_required(self):
        """Test that accessing the dish detail view requires login."""
        res = self.client.get(DISH_DETAIL_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_dish_type_list_required(self):
        """Test that the dish type list view is accessible without login."""
        res = self.client.get(DISH_TYPE_LIST_URL)
        self.assertEqual(res.status_code, 200)
    
    def test_dish_type_list_required(self):
        """Test that the ingredient list view is accessible without login."""
        res = self.client.get(INGREDIENT_LIST_URL)
        self.assertEqual(res.status_code, 200)
    
    def test_about_required(self):
        """Test that the about page is accessible without login."""
        res = self.client.get(ABOUT_URL)
        self.assertEqual(res.status_code, 200)
    
    def test_contact_required(self):
        """Test that the contact page is accessible without login."""
        res = self.client.get(CONTACT_URL)
        self.assertEqual(res.status_code, 200)


class PrivateTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "password123",
        )
        self.client.force_login(self.user)
        self.cook1 = get_user_model().objects.create_user(username="username1", password="password")
        self.cook2 = get_user_model().objects.create_user(username="username2", password="password")
        self.ingredient1 = Ingredient.objects.create(name="ingredient1")
        self.ingredient2 = Ingredient.objects.create(name="ingredient2")
        self.dish_type = DishType.objects.create(name="type_name")
        self.dish = Dish.objects.create(
            name="dish_name",
            description="test_description",
            dish_type=self.dish_type,
            price=12,
        )
        self.dish.cooks.set([self.cook1.id, self.cook2.id])
        self.dish.ingredients.set([self.ingredient1.id, self.ingredient2.id])

    def test_retrieve_dish_list(self):
        """Test that retrieving the dish list returns a 200 status code, the expected list of dishes, and uses the correct template."""
        res = self.client.get(DISH_LIST_URL)
        dishes = Dish.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["dish_list"]), list(dishes))
        self.assertTemplateUsed(res, "kitchen/dish_list.html")

    def test_create_dish_view_get(self):
        """Test accessing the dish create view"""
        res = self.client.get(DISH_CREATE_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "kitchen/dish_form.html")

    def test_create_dish_view_post(self):
        """Test creating a new dish via POST"""
        form_data = {
            "name": "Test Dish",
            "description": "A test dish",
            "price": 12.99,
            "dish_type": self.dish_type.id,
            "cooks": [1,],
            "ingredients": [1,],
        }
        res = self.client.post(DISH_CREATE_URL, data=form_data)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(Dish.objects.filter(name="Test Dish").exists())

    def test_update_dish_view_get(self):
        """Test accessing the dish update view"""
        res = self.client.get(DISH_UPDATE_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "kitchen/dish_form.html")
        self.assertContains(res, "dish_name")

    def test_update_dish_view_post(self):
        """Test updating an existing dish"""
        form_data = {
            "name": "Updated Dish",
            "description": "Updated Description",
            "price": 15.99,
            "dish_type": self.dish_type.id,
            "cooks": [1,],
            "ingredients": [1,],
        }
        res = self.client.post(DISH_UPDATE_URL, data=form_data)
        self.dish.refresh_from_db()
        self.assertEqual(res.status_code, 302)
        self.assertEqual(self.dish.name, "Updated Dish")

    def test_delete_dish_view(self):
        """Test deleting a dish"""
        dish = Dish.objects.create(
            name="Test Dish",
            description="Test Description",
            price=10.99,
            dish_type=self.dish_type,
        )
        url = reverse("kitchen:dish-delete", args=[dish.id])
        res = self.client.post(url)
        self.assertEqual(res.status_code, 302)
        self.assertFalse(Dish.objects.filter(id=dish.id).exists())

    def test_create_dish_type_view_get(self):
        """Test accessing the dish create view"""
        res = self.client.get(DISH_TYPE_CREATE_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "kitchen/dish_type_form.html")

    def test_create_dish_type_view_post(self):
        """Test creating a new dish via POST"""
        form_data = {
            "name": "Test Dish Type",
        }
        res = self.client.post(DISH_TYPE_CREATE_URL, data=form_data)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(DishType.objects.filter(name="Test Dish Type").exists())

    def test_update_dish_type_view_get(self):
        """Test accessing the dish update view"""
        res = self.client.get(DISH_TYPE_UPDATE_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "kitchen/dish_type_form.html")
        self.assertContains(res, "type_name")

    def test_update_dish_type_view_post(self):
        """Test updating an existing dish"""
        form_data = {
            "name": "Updated Dish Type",
        }
        res = self.client.post(DISH_TYPE_UPDATE_URL, data=form_data)
        self.dish_type.refresh_from_db()
        self.assertEqual(res.status_code, 302)
        self.assertEqual(self.dish_type.name, "Updated Dish Type")

    def test_delete_dish_type_view(self):
        """Test deleting a dish"""
        dish_type = DishType.objects.create(
            name="Test Dish Type",
        )
        url = reverse("kitchen:dish-type-delete", args=[dish_type.id])
        res = self.client.post(url)
        self.assertEqual(res.status_code, 302)
        self.assertFalse(DishType.objects.filter(id=dish_type.id).exists())

    def test_create_ingredient_view_get(self):
        """Test accessing the ingredient create view"""
        res = self.client.get(INGREDIENT_CREATE_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "kitchen/ingredient_form.html")

    def test_create_ingredient_view_post(self):
        """Test creating a new ingredient via POST"""
        form_data = {
            "name": "ingredient111",
        }
        res = self.client.post(INGREDIENT_CREATE_URL, data=form_data)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(Ingredient.objects.filter(name="ingredient111").exists())

    def test_update_ingredient_view_get(self):
        """Test accessing the ingredient update view"""
        res = self.client.get(INGREDIENT_UPDATE_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "kitchen/ingredient_form.html")
        self.assertContains(res, "ingredient1")

    def test_update_ingredient_view_post(self):
        """Test updating an existing ingredient"""
        form_data = {
            "name": "Updated Ingredient",
        }
        res = self.client.post(INGREDIENT_UPDATE_URL, data=form_data)
        self.ingredient1.refresh_from_db()
        self.assertEqual(res.status_code, 302)
        self.assertEqual(self.ingredient1.name, "Updated Ingredient")

    def test_delete_ingredient_view(self):
        """Test deleting a ingredient"""
        ingredient = Ingredient.objects.create(
            name="Test Dish Type",
        )
        url = reverse("kitchen:ingredient-delete", args=[ingredient.id])
        res = self.client.post(url)
        self.assertEqual(res.status_code, 302)
        self.assertFalse(Ingredient.objects.filter(id=ingredient.id).exists())
