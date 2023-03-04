from django.contrib import admin


from .models import Pledge, Project, Comment
from users.models import CustomUser 

# Register your models here.

admin.site.register(CustomUser)
