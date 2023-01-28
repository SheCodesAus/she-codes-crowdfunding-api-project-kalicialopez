# Generated by Django 4.1.5 on 2023-01-26 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_remove_project_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='total',
            field=models.DecimalField(decimal_places=2, default=200000.0, max_digits=10),
            preserve_default=False,
        ),
    ]