# Generated by Django 2.2.28 on 2024-01-12 03:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Home_App', '0018_auto_20240111_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart_table',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='order_item_table',
            fields=[
                ('cart_item_id', models.AutoField(primary_key=True, serialize=False)),
                ('food_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home_App.food_table')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home_App.order_table')),
            ],
        ),
    ]
