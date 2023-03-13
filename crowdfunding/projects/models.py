from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

''' Project Model '''


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    goal = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.URLField()
    course_name = models.CharField(max_length=100)
    educational_institution = models.CharField(max_length=100)
    current_occupation_or_industry = models.CharField(max_length=100)
    desired_occupation_or_industry = models.CharField(max_length=100)
    is_open = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    campaign_deadline = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner_projects'
    )
    # total = models.DecimalField(decimal_places = 2, max_digits = 10)
    liked_by = models.ManyToManyField(
        User,
        related_name='liked_projects'
    )

    @property
    def total(self):
        return self.pledges.aggregate(sum=models.Sum('pledge_amount'))['sum']


''' Pledge Model '''


class Pledge(models.Model):
    pledge_amount = models.DecimalField(decimal_places=2, max_digits=10)
    comment = models.CharField(max_length=200)
    anonymous = models.BooleanField(default=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="pledges")
    supporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='supporter_pledges')


''' Comment Model '''


class Comment(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    project = models.ForeignKey(
        'Project',  on_delete=models.CASCADE, related_name='comments')
    commentator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='commentator_comment')
