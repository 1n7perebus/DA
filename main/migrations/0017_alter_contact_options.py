# Generated by Django 4.2.14 on 2024-09-18 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0016_contact_delete_share"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="contact",
            options={"ordering": ["-pub"], "verbose_name": "contact"},
        ),
    ]
