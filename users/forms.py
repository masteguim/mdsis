from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control bg-light border-0',
                'placeholder': 'Nome'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control bg-light border-0',
                'placeholder': 'Sobrenome'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control bg-light border-0',
                'placeholder': 'Email'
            }),
        }