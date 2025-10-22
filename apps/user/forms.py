from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinLengthValidator
from .validators import validate_username, validate_email
from .models import Profile
from django import forms

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=15, validators=[validate_username, MinLengthValidator(5)])
    email = forms.EmailField(validators=[validate_email])
    password1 = forms.CharField(widget=forms.PasswordInput, validators=[MinLengthValidator(8)])
    password2 = forms.CharField(widget=forms.PasswordInput, validators=[MinLengthValidator(8)])

    class Meta:
        model = Profile
        fields = ('username', 'email', 'password1', 'password2')