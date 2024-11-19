from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic

from kitchen.models import Cook, Dish, Ingredient, DishType

from django.urls import reverse_lazy
from kitchen.forms import LoginForm, SignUpForm, CookUpdateForm, IngredientSearchForm, DishTypeSearchForm, CookSearchForm, DishSearchForm


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
    queryset = Dish.objects.all().prefetch_related("cooks", "ingredients")

    def get_context_data(self, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Dish.objects.all()
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    template_name = "kitchen/dish_detail.html"
    login_url="/accountslogin/"


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    template_name = "kitchen/dish_form.html"
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-list")
    login_url="/accountslogin/"


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    template_name = "kitchen/dish_form.html"
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-list")
    login_url="/accountslogin/"


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    template_name = "kitchen/dish_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-list")
    login_url="/accountslogin/"


# Cook
class CookListView(generic.ListView):
    model = Cook
    template_name = "kitchen/cook_list.html"
    paginate_by = 5
    queryset = Cook.objects.prefetch_related("dishes")

    def get_context_data(self, object_list=None, **kwargs):
        context = super(CookListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username")
        context["search_form"] = CookSearchForm(initial={"username": username})
        return context

    def get_queryset(self):
        queryset = Cook.objects.all()
        form = CookSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(username__icontains=form.cleaned_data["username"])
        return queryset


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    template_name = "kitchen/cook_detail.html"
    login_url="/accountslogin/"


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    template_name = "kitchen/cook_form.html"
    form_class = SignUpForm
    success_url = reverse_lazy("kitchen:cook-list")
    login_url="/accountslogin/"


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    template_name = "kitchen/cook_form.html"
    form_class = CookUpdateForm
    success_url = reverse_lazy("kitchen:cook-list")
    login_url="/accountslogin/"


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    template_name = "kitchen/cook_confirm_delete.html"
    success_url = reverse_lazy("kitchen:cook-list")
    login_url="/accountslogin/"


# Ingredient
class IngredientListView(generic.ListView):
    model = Ingredient
    template_name = "kitchen/ingredient_list.html"
    paginate_by = 5

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
    login_url="/accountslogin/"


class IngredientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ingredient
    template_name = "kitchen/ingredient_form.html"
    fields = "__all__"
    success_url = reverse_lazy("kitchen:ingredient-list")
    login_url="/accountslogin/"


class IngredientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ingredient
    template_name = "kitchen/ingredient_confirm_delete.html"
    success_url = reverse_lazy("kitchen:ingredient-list")
    login_url="/accountslogin/"


# DishType
class DishTypeListView(generic.ListView):
    model = DishType
    template_name = "kitchen/dish_type_list.html"
    paginate_by = 5

    def get_context_data(self, object_list=None, **kwargs):
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
    login_url="/accountslogin/"


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    template_name = "kitchen/dish_type_form.html"
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")
    login_url="/accountslogin/"


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "kitchen/dish_type_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-type-list")
    login_url="/accountslogin/"


def about(request):
    return render(request, "kitchen/about.html")


def contact(request):
    return render(request, "kitchen/contact.html")


def register(request):
    print(request.POST)
    form = SignUpForm(request.POST)
    context = {
        "form": form
    }
    return render(request, "registration/register.html", context=context)
