# Generated by Django 4.2.11 on 2024-06-23 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0009_alter_dreams_scale"),
    ]

    operations = [
        migrations.AddField(
            model_name="dreams",
            name="gender",
            field=models.CharField(
                choices=[("Male", "Male"), ("Female", "Female")],
                default="",
                max_length=6,
            ),
        ),
    ]
