# Generated by Django 4.2.1 on 2024-02-24 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0004_women_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='women',
            name='is_published',
            field=models.BooleanField(choices=[(0, 'Не опубликовано'), (1, 'Опубликовано')], default=0),
        ),
    ]