from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic

from kitchen.models import Cook, Dish, Ingredient, DishType

from django.urls import reverse_lazy
from kitchen.forms import LoginForm, SignUpForm


# @login_required
def index(request):
    num_cooks = Cook.objects.all().count()
    num_dishes = Dish.objects.all().count()
    num_dish_types = DishType.objects.all().count()
    num_ingredients = Ingredient.objects.all().count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dish_types": num_dish_types,
        "num_ingredients": num_ingredients,
        "num_visits": num_visits + 1,
    }
    return render(request, "kitchen/index.html",  context=context)


# Dish
class DishListView(generic.ListView):
    model = Dish
    template_name = "kitchen/dish_list.html"
    paginate_by = 5


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    template_name = "kitchen/dish_detail.html"


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    template_name = "kitchen/dish_form.html"
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-list")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    template_name = "kitchen/dish_form.html"
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    template_name = "kitchen/dish_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-list")


# Cook
class CookListView(generic.ListView):
    model = Cook
    template_name = "kitchen/cook_list.html"
    paginate_by = 5


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    template_name = "kitchen/cook_detail.html"


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    template_name = "kitchen/cook_form.html"
    fields = "__all__"
    success_url = reverse_lazy("kitchen:cook-list")


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    template_name = "kitchen/cook_form.html"
    fields = "__all__"
    success_url = reverse_lazy("kitchen:cook-list")


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    template_name = "kitchen/cook_confirm_delete.html"
    success_url = reverse_lazy("kitchen:cook-list")


# Ingredient
class IngredientListView(generic.ListView):
    model = Ingredient
    template_name = "kitchen/ingredient_list.html"
    paginate_by = 5


class IngredientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Ingredient
    template_name = "kitchen/ingredient_detail.html"


class IngredientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ingredient
    template_name = "kitchen/ingredient_form.html"
    fields = "__all__"
    success_url = reverse_lazy("kitchen:ingredient-list")


class IngredientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ingredient
    template_name = "kitchen/ingredient_form.html"
    fields = "__all__"
    success_url = reverse_lazy("kitchen:ingredient-list")


class IngredientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ingredient
    template_name = "kitchen/ingredient_confirm_delete.html"
    success_url = reverse_lazy("kitchen:ingredient-list")


# DishType
class DishTypeListView(generic.ListView):
    model = DishType
    template_name = "kitchen/dish_type_list.html"
    paginate_by = 5


class DishTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = DishType
    template_name = "kitchen/dish_type_detail.html"


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    template_name = "kitchen/dish_type_form.html"
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    template_name = "kitchen/dish_type_form.html"
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "kitchen/dish_type_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


def about(request):
    return render(request, "kitchen/about.html")


def contact(request):
    return render(request, "kitchen/contact.html")


# def login(request):
#     form = LoginForm(request.POST)
#     context = {
#         "form": form,
#     }
#     return render(request, "accounts/login.html", context=context)


def register(request):
    print(request.POST)
    form = SignUpForm(request.POST)
    context = {
        "form": form
    }
    return render(request, "registration/logged_out.html", context=context)
