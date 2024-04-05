# Generated by Django 5.0.2 on 2024-04-05 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('abbreviation', models.CharField(blank=True, max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='SnakeSpecies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('common_name', models.CharField(max_length=255)),
                ('scientific_name', models.CharField(max_length=255)),
                ('image_path', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('venomous', models.BooleanField(default=False)),
                ('states', models.ManyToManyField(related_name='snake_species', to='Identification.state')),
            ],
        ),
    ]
