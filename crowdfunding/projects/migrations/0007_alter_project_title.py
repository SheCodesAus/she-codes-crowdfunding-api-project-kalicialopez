# Generated by Django 4.1.5 on 2023-01-24 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_project_total_alter_pledge_amount_alter_project_goal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]