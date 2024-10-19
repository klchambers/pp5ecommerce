# Generated by Django 4.2.16 on 2024-10-19 09:55

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_grapevariety_name_alter_wine_grape_varieties'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='region',
            options={'ordering': ['country', 'name']},
        ),
        migrations.AlterField(
            model_name='wine',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='image'),
        ),
    ]
