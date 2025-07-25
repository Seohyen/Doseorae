# Generated by Django 4.2.16 on 2025-05-23 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='thread',
            name='hashtags',
            field=models.ManyToManyField(blank=True, to='community.hashtag'),
        ),
    ]
