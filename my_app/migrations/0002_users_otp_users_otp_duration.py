# Generated by Django 4.2.13 on 2024-07-15 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("my_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="users",
            name="otp",
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AddField(
            model_name="users",
            name="otp_duration",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
