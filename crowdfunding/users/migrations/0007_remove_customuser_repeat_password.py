# Generated by Django 4.1.5 on 2023-01-27 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_customuser_repeat_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='repeat_password',
        ),
    ]
