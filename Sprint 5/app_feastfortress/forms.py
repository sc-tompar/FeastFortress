from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2"]

class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'class': 'email', 'placeholder': 'Email', 'autocomplete': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'pwd', 'placeholder': 'Password', 'autocomplete': 'password'}))