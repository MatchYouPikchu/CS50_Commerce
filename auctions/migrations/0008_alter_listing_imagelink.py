# Generated by Django 4.0.3 on 2022-03-26 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_listing_imagelink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='imageLink',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]