# Generated by Django 5.0 on 2024-01-27 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='checked',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
