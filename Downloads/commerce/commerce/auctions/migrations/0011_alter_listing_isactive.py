# Generated by Django 5.0 on 2024-02-05 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_listing_isactive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
    ]
