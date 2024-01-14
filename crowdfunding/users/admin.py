from django.contrib import admin

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .import models
from .models import CustomUser

# Register your models here.



# from projects.models import Project
# admin.site.register(Project)

class CustomUserAdmin(UserAdmin):
    model = CustomUser


admin.site.register(models.CustomUser)