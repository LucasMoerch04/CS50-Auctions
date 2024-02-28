# Generated by Django 5.0 on 2024-01-28 10:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_remove_watchlist_user_watchlist_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='user',
            field=models.ManyToManyField(blank=True, null=True, related_name='watchlistUser', to=settings.AUTH_USER_MODEL),
        ),
    ]