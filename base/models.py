from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=300)
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    age = models.IntegerField()
    username = models.CharField(max_length=300, null=True, blank=True)
    gender = models.CharField(max_length=100,choices=[('male','Male'),('female','Female'),('others','Others')])
    gender = models.CharField(max_length=100, choices=[('male', 'Male'), ('female', 'Female'), ('others', 'Others')])
    address = models.CharField(max_length=300)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
    def name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.email


