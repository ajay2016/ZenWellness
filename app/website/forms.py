from django import forms
from django.core.validators import MinLengthValidator


class LoginForm(forms.Form):
    phone_number = forms.CharField(
        max_length=10,
        validators=[MinLengthValidator(10)],
        widget=forms.TextInput
    )
    password = forms.CharField(
        widget=forms.PasswordInput
    )
