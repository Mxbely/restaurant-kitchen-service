from django.test import TestCase

from kitchen.forms import (
    IngredientSearchForm,
    DishSearchForm,
    DishTypeSearchForm,
)


class FormsTest(TestCase):
    def test_ingredient_search_form(self):
        form_data = {
            "name": "test_name",
        }
        form = IngredientSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_dish_type_search_form(self):
        form_data = {
            "name": "test_name",
        }
        form = DishTypeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_dish_search_form(self):
        form_data = {
            "name": "test_name",
        }
        form = DishSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
