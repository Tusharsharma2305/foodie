# Generated by Django 2.2.28 on 2024-01-12 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home_App', '0019_auto_20240112_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart_table',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
