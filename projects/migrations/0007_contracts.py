# Generated by Django 4.2.1 on 2023-05-18 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0006_remove_project_address"),
    ]

    operations = [
        migrations.CreateModel(
            name="Contracts",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("address", models.CharField(max_length=42)),
                ("name", models.CharField(max_length=80)),
            ],
        ),
    ]