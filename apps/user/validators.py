from django.core.exceptions import ValidationError
from .models import Profile

def validate_username(value):
    """
    Validate that the username is not already taken.
    """
    if Profile.objects.filter(username=value).exists():
        raise ValidationError("Користувач з таким ім'ям вже існує.")

def validate_email(value):
    """
    Validate that the email is not already taken.
    """
    if Profile.objects.filter(email=value).exists():
        raise ValidationError("Користувач з такою електронною поштою вже існує.")