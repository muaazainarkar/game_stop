# Generated by Django 5.0.6 on 2024-07-01 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamestopapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='image'),
        ),
    ]
