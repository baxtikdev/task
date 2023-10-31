# Generated by Django 4.2.3 on 2023-10-31 06:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="userType",
        ),
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.IntegerField(
                choices=[(1, "ADMIN"), (2, "WAITER"), (3, "CLIENT")], default=3
            ),
        ),
    ]