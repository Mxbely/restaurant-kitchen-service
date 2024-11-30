# -*- encoding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Cook


class CookValidationFormMixin:
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control",
            }
        ),
        required=False,
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First name", 
                "class": "form-control"
                }
        ),
        required=False,
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last name",
                "class": "form-control"
                }
        ),
        required=False,
    )
    year_of_experience = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Experience (years)",
                "class": "form-control"
                }
        ),
        required=False,
    )

    def clean_year_of_experience(self):
        year_of_experience = self.cleaned_data.get("year_of_experience")
        if year_of_experience < 0:
            raise forms.ValidationError("Please enter a valid number for experience.")
        return year_of_experience
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and Cook.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    class Meta:
        model = Cook
        fields = ("username", "email", "first_name", "last_name", "year_of_experience")


class CookRegisterForm(UserCreationForm, CookValidationFormMixin):
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password check", "class": "form-control"}
        )
    )

    class Meta(CookValidationFormMixin.Meta):
        fields = CookValidationFormMixin.Meta.fields + ("password1", "password2",)


class CookUpdateForm(forms.ModelForm, CookValidationFormMixin):
    class Meta:
        model = Cook
        fields = ("username", "email", "first_name", "last_name", "year_of_experience")

class CookSearchForm(forms.Form):
    username = forms.CharField(
        label="",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Search by username", "class": "form-control"}
        ),
    )
