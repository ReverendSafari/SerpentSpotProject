# Generated by Django 5.0.2 on 2024-04-07 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAuth', '0006_rename_profilepic_userprofile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='/media/profile_pics/default.jpg', null=True, upload_to='profile_pics/'),
        ),
    ]
