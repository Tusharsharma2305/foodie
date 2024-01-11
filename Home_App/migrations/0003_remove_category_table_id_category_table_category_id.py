# Generated by Django 5.0 on 2023-12-31 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home_App', '0002_alter_category_table_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category_table',
            name='id',
        ),
        migrations.AddField(
            model_name='category_table',
            name='category_id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
