# Generated by Django 4.2.1 on 2023-05-14 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0012_alter_userprofile_friends"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="Gstno",
            field=models.CharField(default=12344567, max_length=50),
            preserve_default=False,
        ),
    ]