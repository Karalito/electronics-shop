# Generated by Django 3.2.8 on 2021-11-11 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_alter_shippingaddress_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='shippingPrice',
        ),
    ]