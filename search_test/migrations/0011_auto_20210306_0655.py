# Generated by Django 3.1.7 on 2021-03-06 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_test', '0010_productsmptt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsmptt',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]