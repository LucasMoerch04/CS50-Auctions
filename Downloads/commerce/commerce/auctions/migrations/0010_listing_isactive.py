# Generated by Django 5.0 on 2024-02-05 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='isActive',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
