# Generated by Django 4.2.11 on 2024-06-19 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_dreams_scale"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dreams",
            name="scale",
            field=models.IntegerField(default=5),
        ),
    ]
