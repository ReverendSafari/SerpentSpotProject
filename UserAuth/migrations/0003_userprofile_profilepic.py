# Generated by Django 5.0.2 on 2024-04-06 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAuth', '0002_userprofile_observations'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profilepic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics'),
        ),
    ]
