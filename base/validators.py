# validators.py
from django.core.exceptions import ValidationError
import re
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\d{10}$',
    message='Contact number must be exactly 10 digits.'
)
def validate_password(value):
    if len(value) < 8:
        raise ValidationError('Password must be at least 8 characters long.')

    if not re.search(r'[A-Z]', value):
        raise ValidationError('Password must contain at least one uppercase letter.')

    if not re.search(r'[a-z]', value):
        raise ValidationError('Password must contain at least one lowercase letter.')

    if not re.search(r'\d', value):
        raise ValidationError('Password must contain at least one number.')

    if not re.search(r'[!@#$%^&*(),.?":{}|<>+ - * = _]', value):
        raise ValidationError('Password must contain at least one special character.')

