# Generated by Django 5.0 on 2024-01-09 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home_App', '0015_reservation_table_booking_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation_table',
            name='customer_id',
        ),
    ]