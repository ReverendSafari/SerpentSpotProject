# Generated by Django 5.0.2 on 2024-04-06 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAuth', '0003_userprofile_profilepic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profilepic',
            field=models.ImageField(blank=True, default='media/profile_pics/default.jpg', null=True, upload_to='profile_pics'),
        ),
    ]
