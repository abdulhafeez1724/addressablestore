# Generated by Django 4.2.7 on 2023-11-24 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_rename_user_loginuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=10)),
                ('package_name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField()),
                ('category', models.CharField(choices=[('bus', 'Bus'), ('bike', 'Bike'), ('character', 'Character')], max_length=20)),
                ('status', models.CharField(choices=[('for_sale', 'For Sale'), ('sold_out', 'Sold Out'), ('pending', 'Pending')], default='for_sale', max_length=20)),
                ('price', models.IntegerField()),
                ('claim', models.BooleanField(default=False)),
                ('listed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.appuser')),
            ],
        ),
        migrations.RemoveField(
            model_name='marketplaceitem',
            name='listed_by',
        ),
        migrations.DeleteModel(
            name='LoginUser',
        ),
        migrations.DeleteModel(
            name='MarketplaceItem',
        ),
    ]