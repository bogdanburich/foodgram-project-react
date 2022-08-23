# Generated by Django 2.2.28 on 2022-08-23 09:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0003_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='subscriber',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
