# Generated by Django 2.2.28 on 2022-09-25 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20220925_1203'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-date_added']},
        ),
        migrations.AddField(
            model_name='recipe',
            name='date_added',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
