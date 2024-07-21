# models.py
from django.db import models
from django.core.validators import MinLengthValidator
from .validators import validate_password, phone_validator
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=300, validators=[MinLengthValidator(8), validate_password])
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    age = models.IntegerField(null=True)
    username = models.CharField(max_length=300, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=[('male', 'Male'), ('female', 'Female'), ('others', 'Others')])
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=10, help_text="Enter a 10-digit contact number")
    name = models.CharField(max_length=600, blank=True, editable=False)
    is_email_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        self.name = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)


    def __str__(self):
        return self.email
