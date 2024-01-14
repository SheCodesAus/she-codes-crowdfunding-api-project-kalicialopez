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
    # @property & annotations
    # insert this to count the sum the amount of pledges to calculate

    @property
    def sum_pledges(self):
        pledge_sum = self.pledges.aggregate(sum=models.Sum("amount"))["sum"]
        if pledge_sum == None:
            return 0
        else:
            return pledge_sum

    @property
    def goal_balance(self):
        return self.goal - self.sum_pledges

    # code to return title name in the drop down
    def __str__(self):
        return self.title



''' Pledge Model '''


class Pledge(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=10)
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
    date_created =     date_created = models.DateTimeField(auto_now_add=True)