# Generated by Django 4.2.16 on 2025-05-26 13:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('community', '0004_thread_like_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='like_users',
            field=models.ManyToManyField(related_name='like_comment', to=settings.AUTH_USER_MODEL),
        ),
    ]
