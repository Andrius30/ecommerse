from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    picture = models.ImageField(default='default.jpg', upload_to='profile_pics')

    REQUIRED_FIELDS = ['password', 'email']
    def __str__(self):
        return self.username