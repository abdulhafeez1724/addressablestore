# Generated by Django 4.2.7 on 2023-11-24 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketplaceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
                ('category', models.CharField(choices=[('bus', 'Bus'), ('bike', 'Bike'), ('character', 'Character')], max_length=20)),
                ('status', models.CharField(choices=[('for_sale', 'For Sale'), ('sold_out', 'Sold Out'), ('pending', 'Pending')], default='for_sale', max_length=20)),
                ('listing_price', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='balance',
        ),
        migrations.RemoveField(
            model_name='user',
            name='store_id',
        ),
        migrations.AddField(
            model_name='user',
            name='unique_id',
            field=models.CharField(blank=True, editable=False, max_length=6, null=True, unique=True),
        ),
        migrations.DeleteModel(
            name='MarketStore',
        ),
        migrations.AddField(
            model_name='marketplaceitem',
            name='listed_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listed_items', to='store.user'),
        ),
    ]