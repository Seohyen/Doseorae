# Generated by Django 4.2.16 on 2025-05-26 05:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
        ('accounts', '0002_customuser_followings'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='interestBook',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='books.book'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='followings',
            field=models.ManyToManyField(related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
    ]
