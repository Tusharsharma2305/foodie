# Generated by Django 5.0 on 2024-01-03 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home_App', '0006_admin_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='customer_table',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email_id', models.CharField(max_length=50)),
                ('dob', models.CharField(max_length=10)),
                ('phone_no', models.CharField(max_length=10)),
                ('user_id', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
    ]
