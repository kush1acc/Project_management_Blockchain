# Generated by Django 4.2.1 on 2023-05-18 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0005_alter_project_address"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="address",
        ),
    ]
