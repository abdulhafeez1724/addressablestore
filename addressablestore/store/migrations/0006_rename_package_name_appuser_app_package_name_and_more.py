# Generated by Django 4.2.7 on 2023-11-27 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_appuser_listing_remove_marketplaceitem_listed_by_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appuser',
            old_name='package_name',
            new_name='app_package_name',
        ),
        migrations.RemoveField(
            model_name='appuser',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='appuser',
            name='user_id',
        ),
        migrations.AddField(
            model_name='appuser',
            name='username',
            field=models.CharField(default=1, max_length=6, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('bus', 'Bus'), ('bike', 'Bike'), ('character', 'Character'), ('parts', 'Parts')], max_length=20),
        ),
    ]
