# Generated by Django 5.1.1 on 2024-09-25 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='newsletter_subscribed',
            field=models.BooleanField(default=True),
        ),
    ]
