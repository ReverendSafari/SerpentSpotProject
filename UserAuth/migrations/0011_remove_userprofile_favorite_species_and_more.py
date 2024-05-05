# Generated by Django 5.0.2 on 2024-04-30 01:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Identification', '0001_initial'),
        ('UserAuth', '0010_userprofile_favorite_species'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='favorite_species',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='favorite_species',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='favoured_by', to='Identification.snakespecies'),
        ),
    ]