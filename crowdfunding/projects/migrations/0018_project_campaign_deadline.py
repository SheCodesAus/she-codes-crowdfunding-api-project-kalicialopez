# Generated by Django 4.1.5 on 2023-02-28 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_project_course_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='campaign_deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]