# Generated by Django 4.2.6 on 2023-11-05 12:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_watchlist_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='listing_status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wins', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owns', to=settings.AUTH_USER_MODEL),
        ),
    ]
