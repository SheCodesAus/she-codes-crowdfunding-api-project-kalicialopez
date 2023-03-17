from django.contrib import admin
from .models import Project, Comment, Pledge


# Register your models here.

# from users.models import CustomUser 
# admin.site.register(CustomUser)

# admin.site.register(Project, Comment, Pledge)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "image", "owner", "goal", "date_created","current_occupation_or_industry", "desired_occupation_or_industry", "description", "course_name", "educational_institution", "is_open",  "campaign_deadline",)


admin.site.register(Project, ProjectAdmin)


class PledgeAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "amount", "comment", "anonymous", "supporter",)


admin.site.register(Pledge, PledgeAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "commentator", "content", "project", 'date_created')


admin.site.register(Comment, CommentAdmin)
