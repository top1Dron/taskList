from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Additional information about User, which is not contain in default django User table. OneToOne relation"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(blank=True, null=True)
    API_KEY = models.CharField(blank=True, null=True, max_length=64)
    API_SECRET = models.CharField(blank=True, null=True, max_length=64)


    def __str__(self):
        return f'User profile {self.user.username}'
