# Generated by Django 4.2.16 on 2024-10-09 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_wine_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='wine',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
