from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=200, null=False, blank=False)
    last_name = models.CharField(max_length=200, null=False, blank=False)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    country_of_residence = models.CharField(max_length=200, blank=True, null=True)
    highest_level_of_education = models.CharField(max_length=200, blank=True, null=True)


    def __str__(self):
        return self.username
    


# Create your models here.

