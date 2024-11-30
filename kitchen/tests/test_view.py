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
        res = self.client.get(INDEX_URL)
        self.assertEqual(res.status_code, 200)

    def test_dish_detail_required(self):
        res = self.client.get(DISH_DETAIL_URL)
        self.assertNotEqual(res.status_code, 200)
    
    def test_about_required(self):
        res = self.client.get(ABOUT_URL)
        self.assertEqual(res.status_code, 200)
    
    def test_contact_required(self):
        res = self.client.get(CONTACT_URL)
        self.assertEqual(res.status_code, 200)


class PrivateTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "password123",
        )
        self.client.force_login(self.user)
        cook1 = get_user_model().objects.create_user(username="username1", password="password")
        cook2 = get_user_model().objects.create_user(username="username2", password="password")
        ingredient1 = Ingredient.objects.create(name="ingredient1")
        ingredient2 = Ingredient.objects.create(name="ingredient2")
        dish_type = DishType.objects.create(name="type_name")
        dish = Dish.objects.create(
            name="dish_name",
            description="test_description",
            dish_type=dish_type,
            price=12,
        )
        dish.cooks.set([cook1, cook2])
        dish.ingredients.set([ingredient1, ingredient2])

    def test_retrieve_dish_list(self):
        res = self.client.get(DISH_LIST_URL)
        dishes = Dish.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["dish_list"]), list(dishes))
        self.assertTemplateUsed(res, "kitchen/dish_list.html")
