# Generated by Django 4.2.11 on 2024-06-21 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0007_remove_dreams_scale"),
    ]

    operations = [
        migrations.AddField(
            model_name="dreams",
            name="scale",
            field=models.IntegerField(default=5),
        ),
    ]
