# Generated by Django 4.2.16 on 2024-10-09 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_grapevariety_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grapevariety',
            name='name',
            field=models.CharField(default='Unknown Grape', max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='wine',
            name='grape_varieties',
            field=models.ManyToManyField(blank=True, related_name='wines', to='products.grapevariety'),
        ),
    ]
