from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import generic

from kitchen.models import Dish, Ingredient, DishType
from accounts.models import Cook

from django.urls import reverse_lazy
from kitchen.forms import (
    IngredientSearchForm,
    DishTypeSearchForm,
    DishSearchForm,
    DishCreateForm,
)
from restaurant_kitchen_service.settings.base import LOGIN_URL


class IndexView(generic.View):
    def get(self, request):
        num_cooks = Cook.objects.count()
        num_dishes = Dish.objects.count()
        num_dish_types = DishType.objects.count()
        num_ingredients = Ingredient.objects.count()
        num_visits = request.session.get("num_visits", 0)
        self.request.session["num_visits"] = num_visits + 1
        context = {
            "num_cooks": num_cooks,
            "num_dishes": num_dishes,
            "num_dish_types": num_dish_types,
            "num_ingredients": num_ingredients,
            "num_visits": num_visits + 1,
        }
        return render(request, "kitchen/index.html", context=context)


# Dish
class DishListView(generic.ListView):
    model = Dish
    template_name = "kitchen/dish_list.html"
    paginate_by = 10

    def get_context_data(self, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Dish.objects.select_related("dish_type").prefetch_related("cooks", "ingredients")
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    template_name = "kitchen/dish_detail.html"
    login_url = LOGIN_URL


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    template_name = "kitchen/dish_form.html"
    form_class = DishCreateForm
    success_url = reverse_lazy("kitchen:dish-list")
    login_url = LOGIN_URL


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    template_name = "kitchen/dish_form.html"
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-list")
    login_url = LOGIN_URL


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    template_name = "kitchen/dish_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-list")
    login_url = LOGIN_URL


# Ingredient
class IngredientListView(generic.ListView):
    model = Ingredient
    template_name = "kitchen/ingredient_list.html"
    paginate_by = 10

    def get_context_data(self, object_list=None, **kwargs):
        context = super(IngredientListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = IngredientSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        form = IngredientSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class IngredientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ingredient
    template_name = "kitchen/ingredient_form.html"
    fields = "__all__"
    success_url = reverse_lazy("kitchen:ingredient-list")
    login_url = LOGIN_URL


class IngredientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ingredient
    template_name = "kitchen/ingredient_form.html"
    fields = "__all__"
    success_url = reverse_lazy("kitchen:ingredient-list")
    login_url = LOGIN_URL


class IngredientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ingredient
    template_name = "kitchen/ingredient_confirm_delete.html"
    success_url = reverse_lazy("kitchen:ingredient-list")
    login_url = LOGIN_URL


# DishType
class DishTypeListView(generic.ListView):
    model = DishType
    template_name = "kitchen/dish_type_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(DishTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishTypeSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = DishType.objects.all()
        form = DishTypeSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    template_name = "kitchen/dish_type_form.html"
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")
    login_url = LOGIN_URL


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    template_name = "kitchen/dish_type_form.html"
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")
    login_url = LOGIN_URL


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "kitchen/dish_type_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-type-list")
    login_url = LOGIN_URL


class AboutView(generic.TemplateView):
    template_name = "kitchen/about.html"


class ContactView(generic.TemplateView):
    template_name = "kitchen/contact.html"
