from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser




# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=20,unique=True)
    email = models.EmailField(unique=True,blank=False)
    first_name = models.CharField(max_length=50,blank=False)
    last_name = models.CharField(max_length=50,blank=False)
    bio = models.CharField(max_length=520,blank=True)
