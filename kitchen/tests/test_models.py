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

    def test_dish_str_and_relations(self):
        cook1 = get_user_model().objects.create_user(
            username="username1", password="password"
        )
        cook2 = get_user_model().objects.create_user(
            username="username2", password="password"
        )
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


class ModelOrderingTest(TestCase):
    def test_ingredient_ordering(self):
        """Test ordering ingredients by name"""
        Ingredient.objects.create(name="ingred2")
        Ingredient.objects.create(name="ingred3")
        Ingredient.objects.create(name="ingred1")
        
        ingredients = Ingredient.objects.all()
        self.assertEqual(
            list(ingredients.values_list("name", flat=True)),
            ["ingred1", "ingred2", "ingred3"]
        )

    def test_dish_type_ordering(self):
        """Test ordering dish types by name"""
        DishType.objects.create(name="type2")
        DishType.objects.create(name="type3")
        DishType.objects.create(name="type1")
        
        dish_types = DishType.objects.all()
        self.assertEqual(
            list(dish_types.values_list("name", flat=True)),
            ["type1", "type2", "type3"]
        )

    def test_dish_ordering(self):
        """Test ordering dishes by name"""
        dish_type = DishType.objects.create(name="type_name")
        Dish.objects.create(name="dish2", dish_type=dish_type, price=7)
        Dish.objects.create(name="dish3", dish_type=dish_type, price=6)
        Dish.objects.create(name="dish1", dish_type=dish_type, price=8)
        
        dishes = Dish.objects.all()
        self.assertEqual(
            list(dishes.values_list("name", flat=True)),
            ["dish1", "dish2", "dish3"]
        )
