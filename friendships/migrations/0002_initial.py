# Generated by Django 4.1.5 on 2023-01-25 10:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('items', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('friendships', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendship',
            name='user_two',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendships', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='friendship',
            name='user_two_items',
            field=models.ManyToManyField(related_name='friendships', to='items.item'),
        ),
    ]