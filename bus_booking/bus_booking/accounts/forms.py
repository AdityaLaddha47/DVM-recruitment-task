from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPES, label="User Type")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

class PassengerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password1", "password2"]