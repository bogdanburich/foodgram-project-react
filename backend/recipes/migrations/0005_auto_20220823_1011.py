# Generated by Django 2.2.28 on 2022-08-23 10:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_follow_subscriber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7, unique=True, validators=[django.core.validators.RegexValidator(message='Provided color code is invalid.', regex='^#(?:[0-9a-fA-F]{3}){1,2}$')]),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(db_index=True, max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='recipe',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='tags', to='recipes.Recipe'),
        ),
    ]
