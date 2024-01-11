# Generated by Django 2.2.28 on 2024-01-11 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Home_App', '0017_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='cart_table',
            fields=[
                ('cart_id', models.AutoField(primary_key=True, serialize=False)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home_App.customer_table')),
                ('food_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home_App.food_table')),
            ],
        ),
    ]
