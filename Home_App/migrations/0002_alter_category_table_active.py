# Generated by Django 5.0 on 2023-12-31 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home_App', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category_table',
            name='active',
            field=models.CharField(max_length=9),
        ),
    ]