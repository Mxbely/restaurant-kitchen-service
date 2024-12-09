from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from accounts.forms import (
    ChangePasswordForm,
    CookRegisterForm,
    CookSearchForm,
    CookUpdateForm,
    LoginForm,
)
from accounts.models import Cook
from restaurant_kitchen_service.settings.base import LOGIN_URL


class LoginView(LoginView):
    form_class = LoginForm
    template_name = "registration/login.html"

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class CookListView(generic.ListView):
    model = Cook
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CookListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username")
        context["search_form"] = CookSearchForm(initial={"username": username})
        return context

    def get_queryset(self):
        queryset = Cook.objects.prefetch_related("cooks_dishes")
        form = CookSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(username__icontains=form.cleaned_data["username"])
        return queryset


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    login_url = LOGIN_URL
    queryset = Cook.objects.prefetch_related("cooks_dishes")


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookRegisterForm
    success_url = reverse_lazy("accounts:cook-list")
    login_url = LOGIN_URL


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookUpdateForm
    success_url = reverse_lazy("accounts:cook-list")
    login_url = LOGIN_URL


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("accounts:cook-list")
    login_url = LOGIN_URL


class RegisterView(generic.View):
    def post(self, request, *args, **kwargs):
        form = CookRegisterForm(self.request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            if user:
                login(self.request, user)
                return redirect("kitchen:index")
        return render(self.request, "registration/register.html", {"form": form})

    def get(self, request, *args, **kwargs):
        form = CookRegisterForm()
        return render(self.request, "registration/register.html", {"form": form})


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy("accounts:cook-list")
    login_url = LOGIN_URL
    template_name = "accounts/cook_form.html"
