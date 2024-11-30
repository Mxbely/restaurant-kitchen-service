from django.contrib.auth import get_user_model
from django.test import TestCase

from kitchen.models import Ingredient, DishType, Dish


class TestModels(TestCase):
    def test_ingredient_str(self):
        ingredient = Ingredient.objects.create(name="name1")
        self.assertEqual(str(ingredient), "name1")

    def test_dish_type_str(self):
        dish_type = DishType.objects.create(name="name1")
        self.assertEqual(str(dish_type), "name1")

    def test_dish_str(self):
        dish_type = DishType.objects.create(name="type_name")
        dish = Dish.objects.create(
            name="name1",
            description="test_description",
            dish_type=dish_type,
            price=12,
        )
        self.assertEqual(str(dish), "name1")
    
    def test_dish_str(self):
        cook1 = get_user_model().objects.create_user(username="username1", password="password")
        cook2 = get_user_model().objects.create_user(username="username2", password="password")
        ingredient1 = Ingredient.objects.create(name="ingredient1")
        ingredient2 = Ingredient.objects.create(name="ingredient2")
        dish_type = DishType.objects.create(name="type_name")
        dish = Dish.objects.create(
            name="name1",
            description="test_description",
            dish_type=dish_type,
            price=12,
        )
        dish.cooks.set([cook1, cook2])
        dish.ingredients.set([ingredient1, ingredient2])

        self.assertEqual(str(dish), "name1")
        self.assertEqual(list(dish.cooks.all()), [cook1, cook2])
        self.assertEqual(list(dish.ingredients.all()), [ingredient1, ingredient2])
