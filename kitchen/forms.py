# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth import get_user_model

from kitchen.models import Dish, Ingredient, DishType


class DishCreateForm(forms.ModelForm):
    dish_type = forms.ModelChoiceField(
        queryset=DishType.objects.all(),
        widget=forms.Select(),
    )
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )
    
    class Meta:
        model = Dish
        fields = (
            "name", 
            "description", 
            "price", 
            "dish_type", 
            "cooks",
            "ingredients",
        )


class IngredientSearchForm(forms.Form):
    name = forms.CharField(
        label="",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Search by name", "class": "form-control"}
        ),
    )


class DishSearchForm(forms.Form):
    name = forms.CharField(
        label="",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Search by name", "class": "form-control"}
        ),
    )


class DishTypeSearchForm(forms.Form):
    name = forms.CharField(
        label="",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Search by name", "class": "form-control"}
        ),
    )
