# Generated by Django 5.0 on 2024-01-02 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home_App', '0004_food_order_table'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Food',
            new_name='food_table',
        ),
    ]
