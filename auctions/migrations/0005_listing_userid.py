# Generated by Django 4.0.3 on 2022-03-20 17:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_listing_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='userId',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_listings', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]