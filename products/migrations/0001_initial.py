# Generated by Django 4.2.16 on 2024-10-08 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('friendly_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('country', models.CharField(max_length=254)),
            ],
            options={
                'unique_together': {('name', 'country')},
            },
        ),
        migrations.CreateModel(
            name='Wine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('friendly_name', models.CharField(max_length=254)),
                ('slug', models.SlugField(max_length=254, unique=True)),
                ('winemaker', models.CharField(max_length=254)),
                ('description', models.TextField(blank=True)),
                ('rating', models.DecimalField(decimal_places=0, max_digits=6, null=True)),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('category', models.ManyToManyField(related_name='wines', to='products.category')),
                ('region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.region')),
            ],
        ),
    ]