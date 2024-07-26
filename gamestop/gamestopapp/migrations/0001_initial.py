# Generated by Django 5.0.6 on 2024-07-01 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('manufacturar', models.CharField(max_length=200)),
                ('category', models.CharField(choices=[('Fighting', 'Fighting'), ('Action', 'Action'), ('Shooter', 'Shooter'), ('Sports', 'Sports'), ('Battle Royale', 'Battle Royale')], max_length=200)),
                ('price', models.IntegerField()),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
    ]
